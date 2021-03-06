# THE REST OF THE PROJECT HERE:
import collections
import re
import pandas as pd
import matplotlib.pyplot as plt


# read the elements of all_lyrics into a list. Use "Writer(s): " as separator because this string appears exactly
# once in every song:
with open('all_lyrics') as f:
    file_list = [word for line in f for word in line.split(sep="Writer(s): ")]

# make a list in which each element is the lyrics of a specific song. use " # " to identify which elements of file_list
# are actual lyrics we want, since " # " appears exactly once in every song:
lyrics_text_list_new = []
for item in file_list:
    if " # " in item:
        lyrics_text_list_new.append(item)

# remove irrelevant contents of the list, so we only keep the song lyrics:
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

# get a list of the words appearing in the lyrics, removing the punctuation marks:
words = []
punctuation = "!&(),.:;?[]"
for item in lyrics_text_list_new:
    temp = item.split(" ")
    for word in temp:
        for i in word:
            if i in punctuation:
                word = word.replace(i, "")
        words.append(word.lower())

# make a dictionary with words as keys and frequencies of these words as values:
counts = dict(collections.Counter(words))

# make a dataframe out of counts dictionary:
words_dataframe = pd.DataFrame(counts.items())
words_dataframe.columns = ['word', 'counts']
words_dataframe = words_dataframe.sort_values(by="counts", ascending=False)

# Pick the 15 most common words, excluding articles, pronouns, prepositions and conjunctions.
# I excluded words like 'in' and 'to' which can often be used as parts of phrasal verbs.
# I also included only the first occurrence of 'to be' verb and not its variations like "i'm", etc.:
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

# plot:
fig = plt.figure()
ax = fig.add_subplot(111)
ax.barh(top_15_words, top_15_counts, color='steelblue')
ax.invert_yaxis()
ax.set_xlabel('Word Counts')
ax.set_title('The 15 most common words in Offspring lyrics')
for i, v in enumerate(top_15_counts):
    ax.text(v - 23, i + .25, str(v), color='white')
plt.show()

# word cloud for 15 most common words selected previously:
top_15_dict = dict(zip(top_15_words, top_15_counts))
wordcloud1 = WordCloud(max_font_size=100).generate_from_frequencies(top_15_dict)
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")
plt.show()

# word cloud for most common words (including articles and other parts of speech I excluded earlier):
wordcloud2 = WordCloud(max_words=500, max_font_size=100, background_color="white").generate_from_frequencies(counts)
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.show()

# word cloud for most common words (including articles and other parts of speech I excluded earlier) in the shape
# of The Offspring logo:
mask = np.array((Image.open("C:/Users/AFRIZ/Desktop/offspring songs/logo.jpg")))
wordcloud3 = WordCloud(mask=mask, background_color="white", max_words=500, width=mask.shape[1], height=mask.shape[0])
wordcloud3.generate_from_frequencies(counts)
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")
plt.show()
