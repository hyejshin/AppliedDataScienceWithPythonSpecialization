
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 3
# 
# In this assignment you will explore text message data and create models to predict if a message is spam or not. 

# In[74]:


import pandas as pd
import numpy as np

spam_data = pd.read_csv('spam.csv')

spam_data['target'] = np.where(spam_data['target']=='spam',1,0)
spam_data.head(10)


# In[75]:


from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(spam_data['text'], 
                                                    spam_data['target'], 
                                                    random_state=0)


# ### Question 1
# What percentage of the documents in `spam_data` are spam?
# 
# *This function should return a float, the percent value (i.e. $ratio * 100$).*

# In[7]:


def answer_one():
    percentage = len(spam_data[spam_data['target']==1]) / len(spam_data) * 100
    
    return percentage


# In[8]:


answer_one()


# ### Question 2
# 
# Fit the training data `X_train` using a Count Vectorizer with default parameters.
# 
# What is the longest token in the vocabulary?
# 
# *This function should return a string.*

# In[80]:


from sklearn.feature_extraction.text import CountVectorizer

def answer_two():
    vect = CountVectorizer().fit(X_train)
    features = vect.get_feature_names()
    longestWord = features[0]
    for word in features:
        if len(word) > len(longestWord):
            longestWord = word
    
    return longestWord


# In[16]:


answer_two()


# ### Question 3
# 
# Fit and transform the training data `X_train` using a Count Vectorizer with default parameters.
# 
# Next, fit a fit a multinomial Naive Bayes classifier model with smoothing `alpha=0.1`. Find the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[121]:


from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score

def answer_three():
    vect = CountVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    
    clf = MultinomialNB(alpha=0.1)
    clf.fit(X_train_vectorized, y_train)

    predictions = clf.predict(vect.transform(X_test))

    auc = roc_auc_score(y_test, predictions)
    
    return auc


# In[122]:


answer_three()


# ### Question 4
# 
# Fit and transform the training data `X_train` using a Tfidf Vectorizer with default parameters.
# 
# What 20 features have the smallest tf-idf and what 20 have the largest tf-idf?
# 
# Put these features in a two series where each series is sorted by tf-idf value and then alphabetically by feature name. The index of the series should be the feature name, and the data should be the tf-idf.
# 
# The series of 20 features with smallest tf-idfs should be sorted smallest tfidf first, the list of 20 features with largest tf-idfs should be sorted largest first. 
# 
# *This function should return a tuple of two series
# `(smallest tf-idfs series, largest tf-idfs series)`.*

# In[35]:


from sklearn.feature_extraction.text import TfidfVectorizer

def answer_four():
    vect = TfidfVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)

    feature_names = np.array(vect.get_feature_names())
    tfidf = X_train_vectorized.max(0).toarray()[0]
    sorted_tfidf_index = X_train_vectorized.max(0).toarray()[0].argsort()
    
    smallestTfidf = feature_names[sorted_tfidf_index[:20]]
    largestTfidf = feature_names[sorted_tfidf_index[:-21:-1]]

    small = pd.Series(tfidf[sorted_tfidf_index[:20]], index=smallestTfidf)
    large = pd.Series(tfidf[sorted_tfidf_index[:-21:-1]], index=largestTfidf)
    
    small = small.iloc[np.lexsort([small.index, small.values])]
    large = large.iloc[np.lexsort([large.index, large.values])]
    
    return (small, large)


# In[36]:


answer_four()


# ### Question 5
# 
# Fit and transform the training data `X_train` using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than **3**.
# 
# Then fit a multinomial Naive Bayes classifier model with smoothing `alpha=0.1` and compute the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[39]:


def answer_five():
    vect = TfidfVectorizer(min_df=3).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    
    clf = MultinomialNB(alpha=0.1)
    clf.fit(X_train_vectorized, y_train)

    predictions = clf.predict(vect.transform(X_test))

    auc = roc_auc_score(y_test, predictions)
    
    return auc


# In[40]:


answer_five()


# ### Question 6
# 
# What is the average length of documents (number of characters) for not spam and spam documents?
# 
# *This function should return a tuple (average length not spam, average length spam).*

# In[41]:


def answer_six():
    spam = spam_data[spam_data['target']==1]
    nonSpam = spam_data[spam_data['target']==0]
    
    spamLengthSum = 0
    for word in spam['text']:
        spamLengthSum += len(word)
        
    nonSpamLengthSum = 0
    for word in nonSpam['text']:
        nonSpamLengthSum += len(word)
    
    return (nonSpamLengthSum/len(nonSpam), spamLengthSum/len(spam))


# In[42]:


answer_six()


# <br>
# <br>
# The following function has been provided to help you combine new features into the training data:

# In[43]:


def add_feature(X, feature_to_add):
    """
    Returns sparse feature matrix with added feature.
    feature_to_add can also be a list of features.
    """
    from scipy.sparse import csr_matrix, hstack
    return hstack([X, csr_matrix(feature_to_add).T], 'csr')


# ### Question 7
# 
# Fit and transform the training data X_train using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than **5**.
# 
# Using this document-term matrix and an additional feature, **the length of document (number of characters)**, fit a Support Vector Classification model with regularization `C=10000`. Then compute the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[62]:


from sklearn.svm import SVC

def answer_seven():
    vect = TfidfVectorizer(min_df=5).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    
    X_train_length = X_train.apply(len)
    X_train_vectorized_added = add_feature(X_train_vectorized, X_train_length)
    
    clf = SVC(C=10000)
    clf.fit(X_train_vectorized_added, y_train)
    
    X_test_vectorized = vect.transform(X_test)
    X_test_length = X_test.apply(len)
    X_test_vectorized_added = add_feature(X_test_vectorized, X_test_length)
    
    predictions = clf.predict(X_test_vectorized_added)

    auc = roc_auc_score(y_test, predictions)

    return auc


# In[63]:


answer_seven()


# ### Question 8
# 
# What is the average number of digits per document for not spam and spam documents?
# 
# *This function should return a tuple (average # digits not spam, average # digits spam).*

# In[64]:


def answer_eight():
    spam = spam_data[spam_data['target']==1]
    nonSpam = spam_data[spam_data['target']==0]
    
    spamDigitSum = 0
    for word in spam['text']:
        for c in word:
            if c.isdigit():
                spamDigitSum += 1
                
        
    nonSpamDigitSum = 0
    for word in nonSpam['text']:
        for c in word:
            if c.isdigit():
                nonSpamDigitSum += 1
    
    return (nonSpamDigitSum/len(nonSpam), spamDigitSum/len(spam))


# In[65]:


answer_eight()


# ### Question 9
# 
# Fit and transform the training data `X_train` using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than **5** and using **word n-grams from n=1 to n=3** (unigrams, bigrams, and trigrams).
# 
# Using this document-term matrix and the following additional features:
# * the length of document (number of characters)
# * **number of digits per document**
# 
# fit a Logistic Regression model with regularization `C=100`. Then compute the area under the curve (AUC) score using the transformed test data.
# 
# *This function should return the AUC score as a float.*

# In[156]:


from sklearn.linear_model import LogisticRegression

def digitCount(word):
    count = 0
    for c in word:
        if c.isdigit():
            count += 1
    return count

def answer_nine():
    vect = TfidfVectorizer(min_df=5, ngram_range=(1,3)).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    
    X_train_length = X_train.apply(len)
    X_train_vectorized_added = add_feature(X_train_vectorized, X_train_length)
    X_train_digit = X_train.apply(digitCount)
    X_train_vectorized_added = add_feature(X_train_vectorized_added, X_train_digit)
    
    model = LogisticRegression(C=100)
    model.fit(X_train_vectorized_added, y_train)
    
    X_test_vectorized = vect.transform(X_test)
    X_test_length = X_test.apply(len)
    X_test_vectorized_added = add_feature(X_test_vectorized, X_test_length)
    X_test_digit = X_test.apply(digitCount)
    X_test_vectorized_added = add_feature(X_test_vectorized_added, X_test_digit)
    
    predictions = model.predict(X_test_vectorized_added)

    auc = roc_auc_score(y_test, predictions)
    
    return auc



# In[157]:


answer_nine()


# ### Question 10
# 
# What is the average number of non-word characters (anything other than a letter, digit or underscore) per document for not spam and spam documents?
# 
# *Hint: Use `\w` and `\W` character classes*
# 
# *This function should return a tuple (average # non-word characters not spam, average # non-word characters spam).*

# In[170]:


import re

def answer_ten():
    spam = spam_data[spam_data['target']==1]
    nonSpam = spam_data[spam_data['target']==0]
    
    spamNonWordSum = 0
    for word in spam['text']:
        regx = re.compile('\W')
        result = regx.findall(word)
        spamNonWordSum += len(result)
                
        
    nonSpamNonWordSum = 0
    for word in nonSpam['text']:
        regx = re.compile('\W')
        result = regx.findall(word)
        nonSpamNonWordSum += len(result)
        
    return (nonSpamNonWordSum/len(nonSpam), spamNonWordSum/len(spam))


# In[171]:


answer_ten()


# ### Question 11
# 
# Fit and transform the training data X_train using a Count Vectorizer ignoring terms that have a document frequency strictly lower than **5** and using **character n-grams from n=2 to n=5.**
# 
# To tell Count Vectorizer to use character n-grams pass in `analyzer='char_wb'` which creates character n-grams only from text inside word boundaries. This should make the model more robust to spelling mistakes.
# 
# Using this document-term matrix and the following additional features:
# * the length of document (number of characters)
# * number of digits per document
# * **number of non-word characters (anything other than a letter, digit or underscore.)**
# 
# fit a Logistic Regression model with regularization C=100. Then compute the area under the curve (AUC) score using the transformed test data.
# 
# Also **find the 10 smallest and 10 largest coefficients from the model** and return them along with the AUC score in a tuple.
# 
# The list of 10 smallest coefficients should be sorted smallest first, the list of 10 largest coefficients should be sorted largest first.
# 
# The three features that were added to the document term matrix should have the following names should they appear in the list of coefficients:
# ['length_of_doc', 'digit_count', 'non_word_char_count']
# 
# *This function should return a tuple `(AUC score as a float, smallest coefs list, largest coefs list)`.*

# In[208]:


def nonWordCount(word):
    text_length = len(re.sub('[\w]+', '', word))
    return text_length

def answer_eleven():
    vect = CountVectorizer(min_df=5, ngram_range=(2,5), analyzer='char_wb').fit(X_train)
    X_train_vectorized = vect.transform(X_train)

    X_train_length = X_train.apply(len)
    X_train_vectorized_added = add_feature(X_train_vectorized, X_train_length)
    X_train_digit = X_train.apply(digitCount)
    X_train_vectorized_added = add_feature(X_train_vectorized_added, X_train_digit)
    X_train_nonWord = X_train.apply(nonWordCount)
    X_train_vectorized_added = add_feature(X_train_vectorized_added, X_train_nonWord)
    
    model = LogisticRegression(C=100,random_state=0, solver='liblinear')
    model.fit(X_train_vectorized_added, y_train)
    
    X_test_vectorized = vect.transform(X_test)
    X_test_length = X_test.apply(len)
    X_test_vectorized_added = add_feature(X_test_vectorized, X_test_length)
    X_test_digit = X_test.apply(digitCount)
    X_test_vectorized_added = add_feature(X_test_vectorized_added, X_test_digit)
    X_test_nonWord = X_test.apply(nonWordCount)
    X_test_vectorized_added = add_feature(X_test_vectorized_added, X_test_nonWord)
    
    predictions = model.predict(X_test_vectorized_added)

    auc = roc_auc_score(y_test, predictions)
    
    sorted_coef_index = model.coef_[0].argsort()
    smallest = model.coef_[0][sorted_coef_index[:10]].tolist()
    largest = model.coef_[0][sorted_coef_index[-10:]].tolist()
    largest = sorted(largest, reverse=True)
    
    return (auc, smallest, largest)


# In[209]:


answer_eleven()


# In[ ]:





# In[ ]:




