# The most common words in The Offspring's lyrics
Since I discovered The Offspring in 2011, they became one of my favourite bands. Soon after discovering the band I learned the lyrics of the majority of their songs inside out, so I had a rough sense of which words appeared the most often in them. I decided to do an analysis of their lyrics after coming accross a post from the r/Metallica subreddit, in which the user Relic827 analyzed Metallica's lyrics and found the most common words in them.   

## Introduction
This project consists of 2 Python files, named lyrics_downloader and lyrics_analysis. In lyrics_downloader, after I found a url which contained the links to all of their lyrics, I scraped the text contained in each one of them and wrote it in a text file named all_lyrics. In lyrics_analysis, I cleaned the text found in all_lyrics, keeping only the lyrics and not the other text found in these links. Then, I created a data frame which contained each word found in the lyrics and the number of times this word appeared. Then, based on that I created a bar chart and a word cloud, which depict the most common words found in the lyrics.   
I chose to divide the project into 2 separate files, because the process of opening all the 149 links takes time (when I run lyrics_downloader it took more than 30 minutes). By writing the contents of these 149 links to all_lyrics file, I was able continue working on the rest of the project without having to wait for so long each time I run the program.

## Collecting the data
Before doing any analysis, I needed to get the lyrics for all of their songs. I scraped all the lyrics from AZLyrics, because of its simple HTML format, which made scraping easier. I extracted all the links for the lyrics found [here](https://www.azlyrics.com/o/offspring.html) using Beautiful Soup and put them in a list, with the following code:   
```
url = "https://www.azlyrics.com/o/offspring.html"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# get links:
links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))
```
The list links contained every link found [here](https://www.azlyrics.com/o/offspring.html), with the links I needed being in the positions between indexes 33 and 182. Also, the relevant links were not clickable, as they started with ".." (for example, the link to the lyrics of the song "Crossroads" was ../lyrics/offspring/crossroads.html, not https://www.azlyrics.com/lyrics/offspring/crossroads.html). With the following code I obtained a list of all the links I needed in the correct format:
```
# get the links for the song lyrics:
lyrics_links_temp = links[33:182]

# change the format of the links in lyrics_links_temp to make them clickable:
lyrics_links = []
for item in lyrics_links_temp:
    temp = ""
    temp = item[2:]
    temp = "https://www.azlyrics.com" + temp
    lyrics_links.append(temp)
```
Next, I defined functions tag_visible and text_from_html, which get the visible text from an HTML document:
```
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
```
Then, I opened each link in lyrics_links and with the help of text_from_html I put the visible text from each link to a list named lyrics_text_list. I made the for loop wait for a random amount of time between 5 and 20 seconds before each iteration (i.e. before opening each link in the list), so I don't create an excessive amount of traffic to the website:
```
# get visible text from all the links:
lyrics_text_list = []
for link in lyrics_links:
    link_html = urllib.request.urlopen(link).read()
    lyrics_text_list.append(text_from_html(link_html))
    sleep(randint(5, 20))
```
Lastly, I wrote the contents of lyrics_text_list to a file named all_lyrics, separating each element of the list from the next with 10 newline characters:
```
# write the contents of lyrics_text_list to a file:
lyrics_file = open("all_lyrics", "w")
for element in lyrics_text_list:
    lyrics_file.write(element + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n")
lyrics_file.close()
```
After this, I continued the project in the second file, lyrics_analysis, so I rewrote the elements of lyrics_file into a list named lyrics_text_list_new. I used the string "Writer(s): " as separator, because this string appeared exactly once in every song:
```
with open('all_lyrics') as f:
    file_list = [word for line in f for word in line.split(sep="Writer(s): ")]
```
In the list file_list, some elements were the lyrics (plus some other text), while other elements were irrelevant parts of visible text from all the links opened previously, which were of no interest. So, I created a new list named lyrics_text_list_new, in which each element is the lyrics of a specific song. I used the string " # " to identify which elements of file_list are the actual lyrics, since " # " appears exactly once in every song:
```
lyrics_text_list_new = []
for item in file_list:
    if " # " in item:
        lyrics_text_list_new.append(item)
```
Next, I removed the irrelevant contents of each element of lyrics_text_list_new, keeping only the lyrics. This was not excessively tricky, since all the elements of lyrics_text_list_new followed certain patterns, which allowed me to use RegEx to clean up the mess:
```
for i in range(len(lyrics_text_list_new)):
    lyrics_text_list_new[i] = re.sub(r'\s+Submit Corrections.+$', "", lyrics_text_list_new[i])
    lyrics_text_list_new[i] = re.sub(r'^\s{18}.+Search\s{42}', "", lyrics_text_list_new[i])
    lyrics_text_list_new[i] = re.sub(r'^\".+\"\slyrics\s{3}The Offspring Lyrics\s{6}\".+\"\s{4}', "",
                                     lyrics_text_list_new[i])
    if "(originally" in lyrics_text_list_new[i]:
        lyrics_text_list_new[i] = re.sub(
            r'^\".+\"\slyrics\s{3}The Offspring Lyrics\s{6}\".+\"\s{2}\(originally.+\)\s{4}'
            , "", lyrics_text_list_new[i])
    if "(from" in lyrics_text_list_new[i]:
        lyrics_text_list_new[i] = re.sub(r'^\".+\"\slyrics\s{3}The Offspring Lyrics\s{6}\".+\"\s{2}\(from.+\)\s{4}', "",
                                         lyrics_text_list_new[i])
```
At this point, each element of lyrics_text_list_new was the lyrics of a song. Then, I created a list of the words appearing in the lyrics, named words, removing the punctuation marks. Based on the words list, I created a dictionary named counts, which had words as keys and frequencies of these words as values:
```
words = []
punctuation = "!&(),.:;?[]"
for item in lyrics_text_list_new:
    temp = item.split(" ")
    for word in temp:
        for i in word:
            if i in punctuation:
                word = word.replace(i, "")
        words.append(word.lower())

counts = dict(collections.Counter(words))
```
To make plotting easier, I created a data frame out of the counts dictionary, named words_dataframe, and sorted it based on counts in descending order:
```
words_dataframe = pd.DataFrame(counts.items())
words_dataframe.columns = ['word', 'counts']
words_dataframe = words_dataframe.sort_values(by="counts", ascending=False)
```
Then, I picked the 15 most common words, excluding articles, pronouns, prepositions and conjunctions. I excluded words like 'in' and 'to' which can often be used as parts of phrasal verbs. I also included only the first occurrence of 'to be' verb and not its variations like "i'm", etc. I put those words and their respective counts in two lists:
```
top_15_words = []
top_15_counts = []
top_15_words.append(words_dataframe['word'][13])
top_15_counts.append(words_dataframe['counts'][13])
top_15_words.append(words_dataframe['word'][49])
top_15_counts.append(words_dataframe['counts'][49])
top_15_words.append(words_dataframe['word'][148])
top_15_counts.append(words_dataframe['counts'][148])
top_15_words.append(words_dataframe['word'][224])
top_15_counts.append(words_dataframe['counts'][224])
top_15_words.append(words_dataframe['word'][115])
top_15_counts.append(words_dataframe['counts'][115])
top_15_words.append(words_dataframe['word'][120])
top_15_counts.append(words_dataframe['counts'][120])
top_15_words.append(words_dataframe['word'][443])
top_15_counts.append(words_dataframe['counts'][443])
top_15_words.append(words_dataframe['word'][105])
top_15_counts.append(words_dataframe['counts'][105])
top_15_words.append(words_dataframe['word'][34])
top_15_counts.append(words_dataframe['counts'][34])
top_15_words.append(words_dataframe['word'][75])
top_15_counts.append(words_dataframe['counts'][75])
top_15_words.append(words_dataframe['word'][834])
top_15_counts.append(words_dataframe['counts'][834])
top_15_words.append(words_dataframe['word'][98])
top_15_counts.append(words_dataframe['counts'][98])
top_15_words.append(words_dataframe['word'][366])
top_15_counts.append(words_dataframe['counts'][366])
top_15_words.append(words_dataframe['word'][231])
top_15_counts.append(words_dataframe['counts'][231])
top_15_words.append(words_dataframe['word'][311])
top_15_counts.append(words_dataframe['counts'][311])
```
I then created the bar chart, based on the contents of top_15_words and top_15_counts, using the following code:
```
fig = plt.figure()
ax = fig.add_subplot(111)
ax.barh(top_15_words, top_15_counts, color='steelblue')
ax.invert_yaxis()
ax.set_xlabel('Word Counts')
ax.set_title('The 15 most common words in Offspring lyrics')
for i, v in enumerate(top_15_counts):
    ax.text(v - 23, i + .25, str(v), color='white')
plt.show()
```
The resulting bar chart is this:   
![Bar chart](https://raw.githubusercontent.com/aphroditerizou/Offspring-lyrics/main/bar%20chart.png)   
   
Next, I created a word cloud for the 15 most common words that appeared in the previous bar chart, using this code:
```
top_15_dict = dict(zip(top_15_words, top_15_counts))
wordcloud1 = WordCloud(max_font_size=100).generate_from_frequencies(top_15_dict)
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")
plt.show()
```
The resulting word cloud is this:   
![Word cloud](https://raw.githubusercontent.com/aphroditerizou/Offspring-lyrics/main/wordcloud%20top%2015.png)   

Then, I created a word cloud for the most common words (including articles and other parts of speech I excluded earlier):
```
wordcloud2 = WordCloud(max_words=500, max_font_size=100, background_color="white").generate_from_frequencies(counts)
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.show()
```
The resulting word cloud is this:   
![Word cloud](https://raw.githubusercontent.com/aphroditerizou/Offspring-lyrics/main/word%20cloud%20top%20500.png)   

Lastly, I created a word cloud for most common words (including articles and other parts of speech I excluded earlier) in the shape of The Offspring logo:
```
mask = np.array((Image.open("C:/Users/AFRIZ/Desktop/offspring songs/logo.jpg")))
wordcloud3 = WordCloud(mask=mask, background_color="white", max_words=500, width=mask.shape[1], height=mask.shape[0])
wordcloud3.generate_from_frequencies(counts)
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")
plt.show()
```
The resulting word cloud is this:   
![Word cloud](https://raw.githubusercontent.com/aphroditerizou/Offspring-lyrics/main/word%20cloud%20logo%20shape.png)   
