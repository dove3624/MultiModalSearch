import urllib2
import csv
import textract
from os import listdir

#r = csv.reader(open("../dataset/urls.txt","r"))

files = listdir("../dataset/audio_text/")

for filename in files:
	#response = urllib2.urlopen("http://www.americanrhetoric.com/" + row[0])
	#fout = open("../dataset/audio_text/" + str(i) + ".mp3", 'wb')
	#fout.write(response.read())
	#fout.close()

	#response = urllib2.urlopen("http://www.americanrhetoric.com/" + row[1])
	#fout = open("../dataset/audio_text/" + str(i) + ".pdf", 'wb')
	#fout.write(response.read())
	#fout.close()

	if 'pdf' in filename:
		text = textract.process("../dataset/audio_text/" + filename, method='pdfminer')
		fout = open("../dataset/audio_text/" + filename[:-4] + ".txt", 'wb')
		fout.write(text)
		fout.close()

