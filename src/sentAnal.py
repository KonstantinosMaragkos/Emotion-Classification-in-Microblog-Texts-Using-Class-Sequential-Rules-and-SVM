#Emotion Classification in Microblog Texts Using Class Sequential Rules
#function main() steps through the program
#prepares the dataset and lexicon and makes call of all the functions


import pandas as pd
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import lexApr as lex
import CSR, subset
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn import svm

def main():

    #Open the datasets
    training_set = "../Data/train_data_red.csv"
    test_set = "../Data/test_data_red.csv"
    val_set = "../Data/val_data_red.csv"
    train_data = pd.read_csv(training_set, engine='python')
    test_data = pd.read_csv(test_set, engine='python')
    val_data = pd.read_csv(val_set, engine='python')
    
    #dropna drops missing values(not available)
    train_data = train_data.dropna(axis=0)
    print (train_data.sentiment.unique())
    test_data = test_data.dropna(axis=0)

    #GET THE RAW FEATURES
    X = train_data.content
    Xtest = test_data.content
    #change the value of sentiment from string to int
    #y = pd.Categorical(pd.factorize(train_data.sentiment)[0])
    switch = {
        'empty': 0,
        'sadness':  1,
        'neutral':  2,
        'surprise':  3,
        'happiness':  4,
        'anger': 5
    }
    y = []
    for s in train_data.sentiment:
        y.append(switch.get(s))

    ytest = []
    for s in val_data.sentiment:
        ytest.append(switch.get(s))

    #Clean the data and replace each seperator with a single fullstop
    #also we use POS tagging for emoticons, urls , @-mentions and hashtags
    print ("POS Tagging and cleaning...")

    #For the training set
    X = [re.sub(r'[^\x00-\x7f]',r' ',s) for s in X]             #remove non-ascii characters
    X = [re.sub(r'https?:\/\/[^ ]*',r'URL',s) for s in X]       #replace urls
    #replace the negative or positive emoticons with tags
    pos_regex = '[:;]-?[)Dp]+|<3'
    neg_regex = ':-?\'?[(/Oo]+'
    X = [re.sub(pos_regex, ' posE ',s) for s in X]
    X = [re.sub(neg_regex, ' negE ',s) for s in X]

    X = [re.sub(r'[.,!;?:]+',r'. ',s) for s in X]             #replace seperators for tokenization
    X = [re.sub(r'#[^ ]*',r'HASHTAG', s) for s in X]          #replace hashtags
    X = [re.sub(r'@[^ ]*',r'AT_MENTION', s) for s in X]       #replace @-mentions
    X = [re.sub("[^A-Za-z_.' ]+",r' ', s) for s in X]

    #For the test set
    Xtest = [re.sub(r'[^\x00-\x7f]',r' ',s) for s in Xtest]             #remove non-ascii characters
    Xtest = [re.sub(r'https?:\/\/[^ ]*',r'URL',s) for s in Xtest]       #replace urls
    #replace the negative or positive emoticons with tags
    Xtest = [re.sub(pos_regex, ' posE ',s) for s in Xtest]
    Xtest = [re.sub(neg_regex, ' negE ',s) for s in Xtest]

    Xtest = [re.sub(r'[.,!;?:]+',r'. ',s) for s in Xtest]             #replace seperators for tokenization

    #Tokenize each microblog text into sentences
    print ("Sentence tokenization...")
    X = [word_tokenize(s) for s in X]
    Xtest = [word_tokenize(s) for s in Xtest]

    #find the sentences that contain conjuction words and split them
    #also hold some extra features for later
    #as the amount of words and the pos/neg emoticons in each tweet
    #open conjuctions.txt and save each word to list
    word_list = [line.rstrip('\n') for line in open("../Data/conjunctions.txt")]

    #For the training set
    XX = []
    posE_train = []
    negE_train = []
    train_len = []
    for tweet in X:
        train_len.append(len(tweet))
        tmp = []
        s = ''
        pose = nege = 0
        for word in tweet:
            if word == 'posE':
                pose += 1
            if word == 'negE':
                nege += 1

            if word in word_list:
                if s != '':
                    tmp.append(s)
                tmp.append(word)
                s = word
            elif word == '.':
                if s != '':
                    tmp.append(s)
                s = ''
            else:
                if s == '':
                    s += word
                else:
                    s += " " + word
        if s != '':
            tmp.append(s)
        XX.append(tmp)
        posE_train.append(pose)
        negE_train.append(nege)

    #For the test set
    XXtest = []
    posE_test = []
    negE_test = []
    test_len = []
    for tweet in Xtest:
        test_len.append(len(tweet))
        tmp = []
        s = ''
        pose = nege = 0
        for word in tweet:
            if word == 'posE':
                pose += 1
            if word == 'negE':
                nege += 1

            if word in word_list:
                if s != '':
                    tmp.append(s)
                tmp.append(word)
                s = word
            elif word == '.':
                if s != '':
                    tmp.append(s)
                s = ''
            else:
                if s == '':
                    s += word
                else:
                    s += " " + word
        if s != '':
            tmp.append(s)
        XXtest.append(tmp)
        posE_test.append(pose)
        negE_test.append(nege)

    print("training set with",len(XX),"tweets")
    print("test set with",len(XXtest),"tweets")

    #-----------------PART 1-----------------#
    #lexicon-based method
    emo = lex.lex(XX)
    emo_test = lex.lex(XXtest)

    #Trasform the training features to ruleitems
    ruleitems = []
    Xvals = []
    for i,v in enumerate(XX):
        tmp = []
        for j,sent in enumerate(v):
            if sent in word_list:
                tmp.append(sent)
            else:
                if emo[i][j][0] == emo[i][j][1]:
                    tmp.append(str(emo[i][j][0]))
                else:
                    tmp.append((str(emo[i][j][0]), str(emo[i][j][1])))
        Xvals.append(tmp)
        ruleitems.append([tmp,y[i]])

    #Transform the test features to condsets
    Xtmp = []
    for i,v in enumerate(XXtest):
        tmp = []
        for j,sent in enumerate(v):
            if sent in word_list:
                tmp.append(sent)
            else:
                if emo_test[i][j][0] == emo_test[i][j][1]:
                    tmp.append(str(emo_test[i][j][0]))
                else:
                    tmp.append((str(emo_test[i][j][0]), str(emo_test[i][j][1])))
        Xtmp.append(tmp)

    #-----------------PART 2-----------------#
    #Minning Class Sequential Rules
    csrs = CSR.CSR_apriori(ruleitems, 0.005, 0.20)
    print(len(csrs))
    #Finall features
    Xtrain = []
    for i,x in enumerate(Xvals):
        tmp = [1 if subset.subset(i,x) else 0 for i in csrs]
        tmp.append(train_len[i])
        tmp.append(posE_train[i])
        tmp.append(negE_train[i])
        Xtrain.append(tmp)

    Xtest = []
    for i,x in enumerate(Xtmp):
        tmp = [1 if subset.subset(i,x) else 0 for i in csrs]
        tmp.append(test_len[i])
        tmp.append(posE_test[i])
        tmp.append(negE_test[i])
        Xtest.append(tmp)

    print(len(Xtrain),len(Xtest))
    print(len(Xtrain[0]),len(Xtest[0]))

    #-----------------PART 3-----------------#
    #TRAINING THE SMV

    #split the training data in order to get a cross validation set
    xtr, xcv, ytr, ycv = train_test_split(Xtrain, y, random_state=42, test_size=0.2)

    #fit the svm using a linear kernel
    print("Training the classifier...")
    svc = svm.LinearSVC(random_state=0,tol=1e-5, max_iter=10000)
    svc = svc.fit(xtr, ytr)

    print("Predicting...")
    prediction = svc.predict(xcv)
    score = f1_score(ycv, prediction, average='micro')
    print("CrossValidation-Set F-score:",score)

    prediction_test = svc.predict(Xtest)
    score = f1_score(ytest, prediction_test, average='micro')
    print("Test-Set F-score:",score)



if __name__ == "__main__":
    main()

