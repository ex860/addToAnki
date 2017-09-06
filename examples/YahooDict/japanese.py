import urllib.request;
from urllib.parse import quote
from bs4 import BeautifulSoup
import subprocess
import platform
import datetime
import json

Collection="C:/Users/hwchiu/AppData/Roaming/Anki2/hwchiu/collection.anki2"
Deck="Test"
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
    reading = ""
    cnt = 0

    print("-------------------------------------------------------------")
    print('<<'+word+'>>')
    print(" ")

    for i in soup.find_all('div', class_='exact_block'):

        firstBlock = i.find('div', class_='concept_light clearfix')
        partJP = firstBlock.find('div', class_='concept_light-wrapper')
        partEN = firstBlock.find('div', class_='concept_light-meanings')

        for j in partJP.find_all('span', class_='furigana'):
            cntt = 0
            for child in j.children:
                print(cntt)
                print(child)
                cntt = cntt + 1
        for j in partJP.find_all('span', class_='text'):
            cntt = 0
            for child in j.children:
                print(cntt)
                print(child)
                cntt = cntt + 1
            front_word += j.get_text()




        for j in partEN.find_all('div', class_="meanings-wrapper"):
            for k in j.find_all('div', class_="meaning-wrapper"):
                cnt = cnt + 1
                back_word += str(cnt)
                back_word += '. '
                for q in k.find_all('span', class_="meaning-meaning"):
                    back_word += q.get_text()
                    back_word += '<br>'

    print('front card='+front_word)
    print('back_card='+back_word)
    if 0 == len(back_word):
        return
    # if "Windows" == platform.system():
    #     subprocess.run(['python', Anki, Collection, Deck, front_word, back_word, reading])
    # else:
    #     subprocess.run(['python3', Anki, Collection, Deck, front_word, back_word, reading])

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