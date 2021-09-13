from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from time import sleep
from random import randint

# this url has the links to all offspring lyrics on AZLyrics:
url = "https://www.azlyrics.com/o/offspring.html"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# get links:
links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

# get the links for the song lyrics:
lyrics_links_temp = links[33:182]

# change the format of the links in lyrics_links_temp to make them clickable:
lyrics_links = []
for item in lyrics_links_temp:
    temp = ""
    temp = item[2:]
    temp = "https://www.azlyrics.com" + temp
    lyrics_links.append(temp)

# get the visible text from these links (exclude tags, etc.):
# return True only for visible text:
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# return visible text:
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    visible_texts_no_spaces = []
    for t in visible_texts:
        visible_texts_no_spaces.append(t.strip())  # strip removes spaces from beginning and end of string
    return u" ".join(visible_texts_no_spaces)  # u" ".join() creates unicode string with " " as separator

# get visible text from all the links:
lyrics_text_list = []
for link in lyrics_links:
    link_html = urllib.request.urlopen(link).read()
    lyrics_text_list.append(text_from_html(link_html))
    sleep(randint(5, 20))

# write the contents of lyrics_text_list to a file:
lyrics_file = open("all_lyrics", "w")
for element in lyrics_text_list:
    lyrics_file.write(element + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n")
lyrics_file.close()

# CONTINUE THIS IN A NEW PYTHON FILE SO I DON'T HAVE TO RUN THE CODE ABOVE REPEATEDLY (IT TAKES VERY LONG TO RUN)
