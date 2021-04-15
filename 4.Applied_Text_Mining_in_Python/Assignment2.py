
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 2 - Introduction to NLTK
# 
# In part 1 of this assignment you will use nltk to explore the Herman Melville novel Moby Dick. Then in part 2 you will create a spelling recommender function that uses nltk to find words similar to the misspelling. 

# ## Part 1 - Analyzing Moby Dick

# In[8]:


import nltk
import pandas as pd
import numpy as np

# nltk.download('punkt')

# If you would like to work with the raw text you can use 'moby_raw'
with open('moby.txt', 'r') as f:
    moby_raw = f.read()
    
# If you would like to work with the novel in nltk.Text format you can use 'text1'
moby_tokens = nltk.word_tokenize(moby_raw)
text1 = nltk.Text(moby_tokens)


# ### Example 1
# 
# How many tokens (words and punctuation symbols) are in text1?
# 
# *This function should return an integer.*

# In[9]:


def example_one():
    
    return len(nltk.word_tokenize(moby_raw)) # or alternatively len(text1)

example_one()


# ### Example 2
# 
# How many unique tokens (unique words and punctuation) does text1 have?
# 
# *This function should return an integer.*

# In[10]:


def example_two():
    
    return len(set(nltk.word_tokenize(moby_raw))) # or alternatively len(set(text1))

example_two()


# ### Example 3
# 
# After lemmatizing the verbs, how many unique tokens does text1 have?
# 
# *This function should return an integer.*

# In[12]:


from nltk.stem import WordNetLemmatizer

# nltk.download('wordnet')

def example_three():

    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w,'v') for w in text1]

    return len(set(lemmatized))

example_three()


# ### Question 1
# 
# What is the lexical diversity of the given text input? (i.e. ratio of unique tokens to the total number of tokens)
# 
# *This function should return a float.*

# In[17]:


def answer_one():
    tokenNum = len(nltk.word_tokenize(moby_raw))
    uniqueTokenNum = len(set(nltk.word_tokenize(moby_raw)))
    
    return uniqueTokenNum/tokenNum

answer_one()


# ### Question 2
# 
# What percentage of tokens is 'whale'or 'Whale'?
# 
# *This function should return a float.*

# In[92]:


def answer_two():
    moby_tokens = nltk.word_tokenize(moby_raw)
    tokenNum = len(moby_tokens)
    whaleNum = 0
    for word in moby_tokens:
        if word == "whale" or word == "Whale":
            whaleNum += 1
        
    return whaleNum/tokenNum*100

answer_two()


# ### Question 3
# 
# What are the 20 most frequently occurring (unique) tokens in the text? What is their frequency?
# 
# *This function should return a list of 20 tuples where each tuple is of the form `(token, frequency)`. The list should be sorted in descending order of frequency.*

# In[35]:


from nltk.probability import FreqDist

def answer_three():
    dist = FreqDist(nltk.word_tokenize(moby_raw))
    words = dist.keys()
    wordlist = []
    for w in words:
        wordlist.append((w, dist[w]))
    wordlist.sort(key = lambda x : x[1], reverse=True)
    return wordlist[:20]

answer_three()


# ### Question 4
# 
# What tokens have a length of greater than 5 and frequency of more than 150?
# 
# *This function should return an alphabetically sorted list of the tokens that match the above constraints. To sort your list, use `sorted()`*

# In[39]:


def answer_four():
    dist = FreqDist(nltk.word_tokenize(moby_raw))
    words = dist.keys()
    wordlist = []
    for w in words:
        if len(w) > 5 and dist[w] >150:
            wordlist.append(w)
    wordlist.sort()
    return wordlist

answer_four()


# ### Question 5
# 
# Find the longest word in text1 and that word's length.
# 
# *This function should return a tuple `(longest_word, length)`.*

# In[42]:


def answer_five():
    words = nltk.word_tokenize(moby_raw)
    longest_word = ''
    length = 0
    for w in words:
        if len(w) > length:
            longest_word = w
            length = len(w)
    return (longest_word, length)

answer_five()


# ### Question 6
# 
# What unique words have a frequency of more than 2000? What is their frequency?
# 
# "Hint:  you may want to use `isalpha()` to check if the token is a word and not punctuation."
# 
# *This function should return a list of tuples of the form `(frequency, word)` sorted in descending order of frequency.*

# In[45]:


def answer_six():
    dist = FreqDist(nltk.word_tokenize(moby_raw))
    words = dist.keys()
    wordlist = []
    for w in words:
        if w.isalpha() and dist[w] > 2000:
            wordlist.append((dist[w], w))
    wordlist.sort(key = lambda x : x[0], reverse=True)
    
    return wordlist

answer_six()


# ### Question 7
# 
# What is the average number of tokens per sentence?
# 
# *This function should return a float.*

# In[59]:


from nltk.tokenize import sent_tokenize

def answer_seven():
    moby_tokens = nltk.word_tokenize(moby_raw)
    sentences = sent_tokenize(moby_raw)
    
    return len(moby_tokens)/len(sentences)

answer_seven()


# ### Question 8
# 
# What are the 5 most frequent parts of speech in this text? What is their frequency?
# 
# *This function should return a list of tuples of the form `(part_of_speech, frequency)` sorted in descending order of frequency.*

# In[68]:


# nltk.download('averaged_perceptron_tagger')

def answer_eight():
    tags = nltk.pos_tag(moby_tokens)
    freq = FreqDist([tag for (word, tag) in tags])
    return freq.most_common(5)

answer_eight()


# ## Part 2 - Spelling Recommender
# 
# For this part of the assignment you will create three different spelling recommenders, that each take a list of misspelled words and recommends a correctly spelled word for every word in the list.
# 
# For every misspelled word, the recommender should find find the word in `correct_spellings` that has the shortest distance*, and starts with the same letter as the misspelled word, and return that word as a recommendation.
# 
# *Each of the three different recommenders will use a different distance measure (outlined below).
# 
# Each of the recommenders should provide recommendations for the three default words provided: `['cormulent', 'incendenece', 'validrate']`.

# In[71]:


from nltk.corpus import words
nltk.download('words')

correct_spellings = words.words()
correct_spellings


# ### Question 9
# 
# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
# 
# **[Jaccard distance](https://en.wikipedia.org/wiki/Jaccard_index) on the trigrams of the two words.**
# 
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

# In[87]:


def answer_nine(entries=['cormulent', 'incendenece', 'validrate']):
    recommandations = []
    correct_spellings = words.words()
    for entry in entries:
        recommand = entry
        distance = 1000
        wordsList = [word for word in correct_spellings if word.startswith(entry[0])]
        
        for w in wordsList:
            dist = nltk.jaccard_distance(set(nltk.ngrams(entry, n=3)), set(nltk.ngrams(w, n=3)))
            if distance > dist:
                recommand = w
                distance = dist
        recommandations.append(recommand)
        
    return recommandations
    
answer_nine()


# 
# ### Question 10
# 
# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
# 
# **[Jaccard distance](https://en.wikipedia.org/wiki/Jaccard_index) on the 4-grams of the two words.**
# 
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

# In[88]:


def answer_ten(entries=['cormulent', 'incendenece', 'validrate']):
    recommandations = []
    correct_spellings = words.words()
    for entry in entries:
        recommand = entry
        distance = 1000
        wordsList = [word for word in correct_spellings if word.startswith(entry[0])]
        
        for w in wordsList:
            dist = nltk.jaccard_distance(set(nltk.ngrams(entry, n=4)), set(nltk.ngrams(w, n=4)))
            if distance > dist:
                recommand = w
                distance = dist
        recommandations.append(recommand)
        
    return recommandations
    
answer_ten()


# ### Question 11
# 
# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
# 
# **[Edit distance on the two words with transpositions.](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)**
# 
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

# In[91]:


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

    return d[lenstr1-1,lenstr2-1]

def answer_eleven(entries=['cormulent', 'incendenece', 'validrate']):
    recommandations = []
    correct_spellings = words.words()
    for entry in entries:
        recommand = entry
        distance = 1000
        wordsList = [word for word in correct_spellings if word.startswith(entry[0])]
        
        for w in wordsList:
            dist = damerau_levenshtein_distance(entry, w)
            if distance > dist:
                recommand = w
                distance = dist
        recommandations.append(recommand)
        
    return recommandations
    
answer_eleven()


# In[ ]:




