#http://flask-restful-cn.readthedocs.org/en/0.3.4/quickstart.html
"""
    This is server program
"""
from flask import Flask, request, jsonify, render_template, url_for, redirect, Markup
from elasticsearch import Elasticsearch
from flask_restful import Resource, Api
import json, urllib, urllib2, unirest, re, pickle
from urllib2 import URLError
import csv
import socket    
import speech_recognition as sr
from nltk.corpus import stopwords
from os import stat

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

def nl2br(txt):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace(u'\r\n', u'<br/>') for p in _paragraph_re.split(txt))
    result = Markup(result)
    return result

fin = open('../dataset/s_to_t.p','rb')
s_to_t = pickle.load(fin)


es = Elasticsearch()
stopwordslist = stopwords.words("english")

result_dic = {}

rev = 0

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub(' ', text)

def remove_unicode(data):
    data = re.sub(r'[^\x00-\x7F]+',' ', data)
    try:
        return data.decode('unicode_escape').encode('ascii','ignore')
    except UnicodeDecodeError:
        return "UnicodeDecodeError"

def es_search(query):
    resrc = es.search(index = 'dbpedia', q = query)
    results =[]
    for hit in resrc['hits']['hits']:
        global rev
        if rev == 0:
            color = 'white'
            rev = 1
        else:
            color = '#e6e6e6'
            rev = 0

        res =  hit["_source"]["resource"]
        temp = Markup("<tr bgcolor=" + color + "> <td> <p>") + nl2br(hit["_source"]["text1"]) + Markup("</p> </td> </tr>")

        rest = es.search(index="test", body={"query": {"match_phrase": {"resource": res}}})
        for img_hit in rest['hits']['hits']:
            temp += Markup("<tr bgcolor=" + color + "> <td> <img src='")  + img_hit['_source']['image'][4:] + Markup("'> </td> </tr>")


        temp += Markup('<tr style="border-bottom: 1px dotted silver;" bgcolor="black"> <td style="width:500px"></td></tr>')

        ht = hash(temp)
        if ht not in result_dic:
            result_dic[ht] = 1
            results.append(temp)

    return results

def only_important_words(word):
    return ' '.join([w for w in word.split() if w not in stopwordslist])

def get_results(query_parts):
    results = []

    if 'query' in query_parts and 'image_classes' in query_parts and 'audio_texts' in 'query_parts':
        query = query_parts['query']
        audio_texts = query_parts['audio_texts']
        image_classes = query_parts['image_classes']

        for aud_txt in audio_texts:
            for img_txt in image_classes:
                query = only_important_words(query) + ' ' + only_important_words(img_txt) + ' ' + only_important_words(aud_txt)
                r = es_search(query)
                results  += r

    elif 'query' in query_parts and 'image_classes' in query_parts:
        query = query_parts['query']
        image_classes = query_parts['image_classes']

        for img_txt in image_classes:
            query = only_important_words(query) + ' ' + only_important_words(img_txt)  
            r = es_search(query)
            results  += r

    elif 'query' in query_parts and 'audio_texts' in query_parts:
        query = query_parts['query']
        audio_texts = query_parts['audio_texts']

        for aud_txt in audio_texts:
            query = only_important_words(query) + ' '  + only_important_words(aud_txt)
            r = es_search(query)
            results  += r

    elif 'audio_texts' in query_parts and 'image_classes' in query_parts:
        audio_texts = query_parts['audio_texts'] 
        image_classes = query_parts['image_classes']

        for aud_txt in audio_texts:
            for img_txt in image_classes:
                query =  only_important_words(img_txt) + ' ' + only_important_words(aud_txt)
                r = es_search(query)
                results  += r

    elif 'audio_texts' in query_parts:
        audio_texts = query_parts['audio_texts']

        for aud_txt in audio_texts:
            query = only_important_words(aud_txt)
            r = es_search(query)
            results  += r

    elif 'image_classes' in query_parts:
        image_classes = query_parts['image_classes']

        for img_txt in image_classes:
            query = only_important_words(img_txt)
            r = es_search(query)
            results  += r

    elif 'query' in query_parts:
        query = query_parts['query']

        query = only_important_words(query)
        r = es_search(query)
        results  += r


    #print results_images
    return results

def get_audio_text(f_sz):
    result = []
    if f_sz in s_to_t:
        text = s_to_t[f_sz]

        global rev
        if rev == 0:
            color = 'white'
            rev = 1
        else:
            color = '#e6e6e6'
            rev = 0

        text = remove_tags(text)
        text = remove_unicode(text)

        text = Markup("<tr bgcolor=" + color + "> <td> <p>") + nl2br(text) + Markup("</p> </td> </tr>")


        text += Markup('<tr style="border-bottom: 1px dotted silver;" bgcolor="black"> <td style="width:500px"></td></tr>')

        result.append(text)

    return result

   

def speech_to_text(filename):
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source) # read the entire audio file

    results = []

    # recognize speech using Sphinx
    try:
        rec = r.recognize_sphinx(audio)
        #print("Sphinx thinks you said " + rec)
        results.append(rec)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        rec = r.recognize_google(audio)
        #print("Google Speech Recognition thinks you said " + rec)
        results.append(rec)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    
    # recognize speech using Wit.ai
    WIT_AI_KEY = "GAQWXWFLZMWSCUKP2WMO3KQTZDAM66KV" # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
    	rec = r.recognize_wit(audio, key=WIT_AI_KEY)
        #print("Wit.ai thinks you said " + rec)
        results.append(rec)
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    # recognize speech using IBM Speech to Text
    IBM_USERNAME = "3a76480e-888a-4b8a-a01c-ed0b9052ca7a" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    IBM_PASSWORD = "DZdATPVunbEj" # IBM Speech to Text passwords are mixed-case alphanumeric strings
    try:
    	rec = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        #print("IBM Speech to Text thinks you said " + rec)
        results.append(rec)
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
    
    return results

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    results = []

    txt = request.form['textInput']
    img =request.files['imageFile']
    aud = request.files['audioFile']

    query_parts = {}

    query = ''

    if txt:
        query = txt
        query_parts['query'] = txt
        print query

    image_classes = []
    if img:
        print img.filename
        img.save("uploads/images/"+img.filename)        
        s = socket.socket()             
        host = socket.gethostname()     
        port = 9999                   
        s.connect((host, port))         
        s.send(img.filename)            
        img_class=s.recv(1024)
        s.close()       
        #print img_class
        image_classes = img_class.split(',')
        query_parts['image_classes'] = image_classes

    if aud:
        aud.save("uploads/audios/" + aud.filename)
        results += get_audio_text(stat("uploads/audios/" + aud.filename).st_size)
        audio_texts = speech_to_text("uploads/audios/" + aud.filename.encode('ascii','ignore'))
        print audio_texts
        query_parts['audio_texts'] = audio_texts

    results += get_results(query_parts)	

    #print results
    #query = query + ' ' + img_class			
    						
        

    #return jsonify({'results_text':results_text, 'results_images':results_images})
    return render_template('index.html', results = results)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.run(debug=True)