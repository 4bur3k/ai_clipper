import requests
import urllib.request
import re
from bs4 import BeautifulSoup

fileFormat = '.mp3'
audioFold = 'audio/'  # collect new music files in this addres. You can stay it empty
while True:
    songname = input()  # Print song name (sometimes it is better to add group name either like "Du hast Rammstein")
    sitename = 'https://ru.hitmotop.com/search?q='
    request = requests.get(sitename + songname.replace(' ', '+'))
    soup = BeautifulSoup(request.content, 'html.parser')  # got sitepage as special object

    try:
        a = soup.find_all('a', href=re.compile(r'http.*\.mp3'))[0]  # find all music links, but we'll get only first res
    except IndexError:
        print("ERROR: There is no music with such name. Try again, please.")
        continue  # user must print song name again if he has an error
    filename = songname.title().replace(' ', '_') + fileFormat
    doc = requests.get(a['href'])
    with open(audioFold + filename, 'wb') as f:
        f.write(doc.content)
    break  # if there was not error then finish parser
