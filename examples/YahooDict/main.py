import urllib.request;
from bs4 import BeautifulSoup
import subprocess

Collection="/Users/hwchiu/Library/Application Support/Anki2/User 1/collection.anki2"
Deck="Novel"
Anki="../../add_to_anki-2.0.12.py"

def look_up_from_yahoo(word):
    """This function will lookup the @input(word) from the yahoo dict"""
    url="https://tw.dictionary.yahoo.com/dictionary?p={}".format(word)
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    front_word = word + "<br>"
    back_word = ""

    print('current word = {}'.format(word))
    for i in soup.find_all('span', {'id':'pronunciation_pos'}):
        front_word += i.get_text()
    for i in soup.find_all('div', {'class':'explain'}):
        wordType = i.find_all('div', {'class':'compTitle'})
        wordDefi = i.find_all('ul', {'class':'compArticleList'})
        for i in range(0,len(wordType)):
            back_word += wordType[i].get_text() +"<br>"
            for q in wordDefi[i]:
                back_word += q.get_text() + "<br>"
    print('front card={}'.format(front_word))
    print('back_card={}'.format(back_word))
    if 0 == len(back_word):
        return
    subprocess.run(['python3', Anki, Collection, Deck, front_word, back_word])
with open("./input", "r") as file:
    for word in file:
        look_up_from_yahoo(word)
