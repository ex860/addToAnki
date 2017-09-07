import urllib.request;
from urllib.parse import quote
from bs4 import BeautifulSoup
import subprocess
import platform
import datetime
import json
import wget
import re
from re import compile as _Re

_unicode_chr_splitter = _Re( '(?s)((?:[\u2e80-\u9fff])|.)' ).split

# Download_dir="C:/Users/Yu-Hsien/AppData/Roaming/Anki2/YuHsien/collection.media/"
Download_dir="/home/yu/.local/share/Anki2/YuHsien/collection.media/"
Anki="../../addToAnkiJapanese.py"

def look_up_from_yahoo(word, Collection, Deck):
    # Eliminate the end of line delimiter
    word = word.splitlines()[0]
    wordUrl = urllib.parse.quote(word, safe='')
    url="http://jisho.org/search/{}".format(wordUrl)
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    front_word = ""
    back_word = ""
    furi = ""
    furiChild = []
    furiList = []
    text = ""
    textChild = []
    textList = []
    reading = ""
    cnt = 0

    print("-------------------------------------------------------------")
    print('<<'+word+'>>')
    print(" ")

    for i in soup.find_all('div', class_='exact_block'):

        firstBlock = i.find('div', class_='concept_light clearfix')
        partJP = firstBlock.find('div', class_='concept_light-wrapper')
        partEN = firstBlock.find('div', class_='concept_light-meanings')

        status = partJP.find('div', class_='concept_light-status')
        if(status != None):
            audio = status.find('audio')
            if(audio != None):
                source = audio.find('source')
                wget.download(source['src'], out=Download_dir+"Jp_"+word+".mp3")
                # Insert the sound media into the card
                front_word = "[sound:Jp_"+word+".mp3]" + word + "<br>"

        for j in partJP.find_all('span', class_='furigana'):
            furiCnt=0
            for child in j.children:
                furiChild.append(child.string)
                furiCnt = furiCnt + 1
            furiList = list(filter(("\n").__ne__, furiChild))
            print("furiList = ",furiList)
        for j in partJP.find_all('span', class_='text'):
            textCnt = 0
            for child in j.children:
                textChild.append(child.string)
                textCnt = textCnt + 1
            for k in range(0,len(textChild)):
                for chr in _unicode_chr_splitter( textChild[k] ):
                    if chr != '\n' and chr != ' ' and chr != '':
                        textList.append(chr)
            print("textList = ",textList)
        
        for j in range(0,len(textList)):
            if(furiList[j] == None):
                reading += textList[j] 
            else:
                reading += " " + textList[j] + "[" + furiList[j] + "]" 
        for j in partEN.find_all('div', class_="meanings-wrapper"):
            for k in j.find_all('div', class_="meaning-wrapper"):
                cnt = cnt + 1
                back_word += str(cnt) + '. '
                for q in k.find_all('span', class_="meaning-meaning"):
                    back_word += q.get_text() + '<br>'

    #print('front card='+front_word)
    #print('back_card='+back_word)
    print("reading=",reading)
    if 0 == len(back_word):
        return
    if "Windows" == platform.system():
       subprocess.run(['python', Anki, Collection, Deck, front_word, back_word, reading])
    else:
       subprocess.run(['python3', Anki, Collection, Deck, front_word, back_word, reading])

count=0
with open('config_J.json', encoding='utf-8') as data_file:
    data = json.load(data_file)

start_time=datetime.datetime.now().replace(microsecond=0)
for profile in data["profiles"]:
    with open(profile["file"], "r", encoding='utf-8') as file:
		# Get the word from each line in file
        for word in file:
            count += 1
            look_up_from_yahoo(word, profile["collection"], profile["deck"])

end_time=datetime.datetime.now().replace(microsecond=0)
print("-------------------------------------------------------------")        
print("Takes {} to add {} cards".format(end_time - start_time ,count))