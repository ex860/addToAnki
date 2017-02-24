import __builtin__
import urllib2
import os.path, time
from dateutil import parser
from bs4 import BeautifulSoup

def LookUpFromYahoo(word):
    url="https://tw.dictionary.yahoo.com/dictionary?p={}".format(word)
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    print 'current word = {}'.format(word)
    for i in soup.find_all('span', {'id':'pronunciation_pos'}):
        print i.get_text()
    for i in soup.find_all('div', {'class':'explain'}):
        wordType = i.find_all('div', {'class':'compTitle'})
        wordDefi = i.find_all('ul', {'class':'compArticleList'})
        for i in range(0,len(wordType)):
            print wordType[i].get_text()
            for q in wordDefi[i]:
                print q.get_text()
    print '--------------------'

with open("input", "r") as file:
    for word in file:
        LookUpFromYahoo(word)


