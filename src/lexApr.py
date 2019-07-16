#This is the lexicon-based method for sentimental analysis
#This part gets an array of sentences and a lexicon
#For each word in a sentence we replace it with the coresponding emotion value from the lexicon
#We count the number of emotion words occurring in a tweet for each emotion type
#and then the emotion label of the text is simply determined
#as the emotion type with the largest number of emotion words appearing in the text

import pandas as pd
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import collections as cl
from operator import add

def lex(X):
    
    #open the lexicon
    lexicon = "../Data/NRC-Emotion-Lexicon-v0.92-English.csv"
    print("LEXICON-BASED METHOD WITH LEXICON: NRC-Emotion-Lexicon-v0.92-English.csv")
    print("Opening the lexicon...")
    lex_data = pd.read_csv(lexicon, engine='python')
    emos = ['Anger','Joy','Sadness','Surprise']
    #Save the data to a faster dataframe
    word_dict = cl.defaultdict()
    for row in lex_data.itertuples():
        word_dict[row.English] = [row.Anger, row.Joy, row.Sadness, row.Surprise]

    #tokenize them and for each word create a tuple
    #with the word and the number of times it exists in the tweet
    print ("Tokenizing...")
    tokens = []
    for text in X:
        tmp = []
        for sent in text:
            tmp.append([w.lower() for w in word_tokenize(sent)])
        tokens.append(tmp)

    print ("Creating the tuple...")
    tuples = []
    for sent in tokens:
        tmp = []
        for lst in sent:
            count = Counter(lst)
            tmp.append(count.most_common(len(count)))
        tuples.append(tmp)

    print ("Finding the sentiment...")
    results = []
    #for each sentence
    for text in tuples:
        tmp = []
        #for each word list of the text
        for lst in text:
            vals = []
            #for each word in the list
            for word, count in lst:
                if word_dict.get(word):
                    #if this word is in the lexicon add the real values
                    tval = [i * count for i in word_dict[word]]
                else:
                    #if not then add 0 values
                    #word 'aback' has 0 values
                    tval = word_dict['aback']
                if len(vals) == 0:
                    vals = tval
                else:
                    vals = list(map(add, vals, tval))

            tmp.append(vals)
        results.append(tmp)

    #find the 2 most domimant sentiments for each sentence
    em = []
    for text in results:
        tmp = []
        for sent in text:
            m1 = m2 = 0.0
            m1c = m2c = -1
            for i,x in enumerate(sent):
                if x > m2:
                    if x > m1:
                        m1, m2 = x, m1
                        m1c, m2c = i, m1c
                    else:
                        m2 = x
                        m2c = i
            tmp.append([m1c, m2c])
        em.append(tmp)
    #Map lexicon values to test and training set values
    for text in em:
        tmp = []
        for sent in text:
            for i,x in enumerate(sent):
                sent[i] = replace(x)

    return em

def replace(x):
    switch = {
        -1: 0,
        0:  5,
        1:  4,
        2:  1,
        3:  3
    }
    return switch.get(x)

