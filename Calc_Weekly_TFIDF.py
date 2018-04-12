#Calc_Weekly_TFIDF.py
# created by Andrew Larkin
# for Scoial Media Analytics course project
# December 5, 2017

# This script partitions Tweets from a raw csv file into weekly subsets,
# writes the subsets to text files, and calculates weekly idf scores
# for for each subset using trigrams


########## Setup ###########

# import modules 
import pandas as ps
from datetime import datetime
from copy import deepcopy as dc
from collections import defaultdict
import nltk as nk
from sklearn.feature_extraction.text import TfidfVectorizer

# define input and output
parentFolder = 'fullParentFilepath' #folder containing all project files"
outputFolder = parentFolder + 'outputFolderpath' # folder where weely partitions of twitter dataset are creatd as csvs
inputFile = parentFolder + 'inputfilename.csv' # input file containing all tweets included in the analysis.  See example tweets for csv column names and order



############## Helper Functions ###############



# convert timestamp to Julian day of the year (1-365)
# INPUTS:
#    dateString (str) - unique string format of the date as shown in the function.  Note the 'T' separating the date and timpe components of the string
# OUTPUTS:
#   Julian day of year, in integer format
def getDayOfYear(dateString):
    return int(datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S").strftime('%j'))


# if a string contains a hyperlink, find the location and remove for downstream text processing
# INPUTS: 
#    inputString (str) - raw text of a tweet, including hyperlinks, emojois, and other author markups.
# OUTPUTS:
#    input string without hyperlink text
def findHttp(inputString):
    httpLoc = str.find(inputString,"http")
    if(httpLoc > -1):
        return(inputString[0:httpLoc])
    else:
        return(inputString)


# partition tweet dataset by day
# INPUTS:
#   dataset 
# OUTPUTS:
#   accumDay 
#   numObs (int) - number of tweets in the day.
def getTextForDay(dataset):
    accumDayText = ""
    numObs = 0
    numTweets = len(dataset['text']) # number of tweets to analyze.  May differ from the number of tweets returend if there are duplicates
    stringList = list(dataset['text']) # extract tweet text attribute from dictionary and convert to a list. 
    
    # for each tweet, remove decoartors and hyperlinks and test for redundancy (i.e. dupliate tweets with small diferences such as a new hyperlink).
    for singleText in range(0,numTweets):
        newString = stringList[singleText]
        newString = findHttp(newString)
        if(newString not in accumDayText):
            
            # test if the new Tweet content is not a duplicate.  
            # Igrnoing decoartions in the first and last three words of the tweet, middle content of the tweet must differ.
            shouldCopy = True
            words1 = list((newString.split()))
            testList = ' '.join(words1[1:max(len(words1)-3,3)])
            
            # if text is unique add to daily tweet set
            if(testList in accumDayText):
                shouldCopy = False
            if(shouldCopy):
                accumDayText += newString
                accumDayText += ".\n"   
                numObs +=1
            
    return([accumDayText,numObs])


# patition tweet dataset by week
# INPUTS:
#   rawData (pandas dataframe) - Pandas data frame containing the entire set of tweets read from the origina input .csv
# OUTPUTS:
#   accumWeekTexts (string array) - each array index contains combined text for all tweets for the corresponding week 
#   e.g. index 0 contains text of all tweets for week 0.
def partitionWeeklyTweets(rawData):
    rawData['dayOfYear'] = list(map(getDayOfYear, rawData['created']))
    uniqueDays = list(set(rawData['dayOfYear']))    # extract Julian day of year from timestamp
    accumTexts = []    
    accumWeekTexts = [""]
    numObs = [0]*len(uniqueDays)
    weekCounter = 0
    weekIndex = 0
    numWeekley = 0

    # for each day of year, copy the tweets text for the given day and add them to the current week's cumulation of tweet text.  
    # Once day 7 is reached, start a new string to hold tweet texts for the next week.
    for dayIndex in range(0,len(uniqueDays)):
        tempCopy = dc(rawData)
        tempData = tempCopy.loc[tempCopy['dayOfYear'] == uniqueDays[dayIndex]]
        [dayText,numObs[dayIndex]] = getTextForDay(tempData)
        accumTexts.append(dayText)
        accumWeekTexts[weekIndex] += dayText
        weekCounter+=1
        numWeekley += numObs[dayIndex]
        # if new week, rest counter and start adding daily tweets to new week subset
        if(weekCounter == 7):
            weekIndex+=1
            weekCounter = 0
            print("num weekley" + str(weekIndex) + " : " + str(numWeekley))
            numWeekley = 0
            accumWeekTexts.append("")
    
    # print(" total number of observations: " + str(sum(numObs)))
    for index in range(0,len(numObs)):
        if(numObs[index] < 100):    # identify days with less than 100 tweets.  Used for first pass at identifying days with incomplete coverage
            print(" less than 100 tweets for day" + str(index))
            
    return(accumWeekTexts)


# output weekly tweet partitions into a set of csvs.  Partitions contain only the tweet texst.
# INPUTS:
#   accumWeekText (array) - an array weekly tweet texts.  Each index in the array contains all tweets for one week.  
def writeWeeklySet(accumWeekTexts):
    weekIndex = 0
    for weekText in accumWeekTexts:
        f = open(outputFolder + "week" + str(weekIndex) + ".txt",'w', encoding='utf8')
        f.write(weekText)
        f.close()
        weekIndex+=1    


# calculate tfidf scores for entire dataset, grouped by week.  Based on script created by Mark Needham
# http://www.markhneedham.com/blog/2015/02/15/pythonscikit-learn-calculating-tfidf-on-how-i-met-your-mother-transcripts/
def calc_tfidf(accumTexts):
    
    # convert text into trigrams an create a word frequency vector.  Adjust weights of vector using TF-IDF.
    tf = TfidfVectorizer(analyzer='word', ngram_range=(3,3),min_df = 0,stop_words = 'english',use_idf=False)     
    tfidf_matrix =  tf.fit_transform(accumTexts)
    feature_names = tf.get_feature_names() 
    dense = tfidf_matrix.todense()
    
    # for each week in the year of data, order the trigrams by TF-IDF score and print out the highest TF-IDF score.
    for weekIndex in range(0,len(accumTexts)):
        weekSet = dense[weekIndex].tolist()[0]
        phrase_scores = [pair for pair in zip(range(0, len(weekSet)), weekSet) if pair[1] > 0]
        sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
        maxScore = max(sorted_phrase_scores)
        first = True
        for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:10]:
                if(first):
                    print(str(weekIndex) + "," + phrase + "," + str(score))
                    first = False # note: you can comment out this line to print the top 10 TF-IDF scores rather than just the first






################### Main Script ##########


def main():
    rawData = ps.read_csv(inputFile,encoding = 'utf8')   # used utf-8 to capture emojis, which were not recognized by default encoding
    accumWeekTexts = partitionWeeklyTweets(rawData) # partition entire dataset into weekly subsets
    writeWeeklySet(accumWeekTexts) # output weekly partitions into a set of csvs.  Output CSVs are used by the Stanford NLP parser for POS tagging.
    calc_tfidf(accumWeekTexts) # calculate TF-IDF scores for each weekly partition.

main()


# end of calcWeekly_tfidf