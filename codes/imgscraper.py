import re
import urllib2
import cPickle

DIR = "americanlibraries/"

articles = []
for i in range(1,50):
   
    cur_page = urllib2.urlopen('https://archive.org/details/americana?and[]=mediatype%3A"image"&sort=-downloads&page='+str(i))
    print cur_page
    html = cur_page.read()
    #articles += re.findall(r'<img class="item-img" style="height:293px" src="/services/img/(.+?)">', html)
    articles += re.findall(r'<img class="item-img" source="/services/img/(.+?)"', html)
    print articles

print len(articles)


cPickle.dump(articles, open('imglib.p','wb'))

articles = cPickle.load(open('imglib.p','rb'))

for article in articles:
    urllib.urlretrieve("https://ia801308.us.archive.org/6/items/"+ article +"/" + article + "_access.jpg", article + ".jpg")
