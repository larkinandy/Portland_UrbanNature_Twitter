# Vader.py
# Created by Andrew Larkin
# for Social Media Analytics course project
# December 5, 2017

# This script uses the vader algorithm in the Python NLTK library to 
# predict the probability that a week's worht of tweets are negative, netural, or positive, as well as the 
# overall predicted sentiment as a weighted average of the negative, netural, and positive
# sentiment predictions

###### SETUP - import libraries, define constants and filepaths ######
import nltk.sentiment.util as that
import nltk.sentiment as sent
import os

parentFolder = "H:/Twitter/SMAProject/SecondAnalysis_Apr8_18/"
inputFolder = parentFolder + "weekly/"


##### MAIN SCRIPT #########

# each week of tweets is stored as a separate file
inputFiles = sorted(os.listdir(inputFolder))
sentimentScores = [0]*len(inputFiles)
fileIndex = 0
weekNums = [0]*len(inputFiles)

# for each batch of weekly tweets, read inthe data, calculate the sentiment for each tweet one at a time, 
# and keep a running track of the mean sentiment
for inputFile in inputFiles:
    fileToProcess = inputFolder + inputFile
    fStream = open(fileToProcess, encoding = "utf8")
    rawData = fStream.read()
    fStream.close()
    endLine = rawData.find("\n")
    totalScore = 0
    numReads = 0
    startLoc = 0
    endLoc = 1
    weekNumStart = inputFile.find("week")
    weekNumEnd = inputFile.find(".txt")
    weekNums[fileIndex] = weekNum = int(inputFile[weekNumStart+4:weekNumEnd])
    while(endLoc>0):
        endLoc = rawData.find("\n",startLoc+1)
        singleTweet = rawData[startLoc:endLoc]    
        try:
            tweetScore= sent.vader.SentimentIntensityAnalyzer(lexicon_file='sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt').polarity_scores(singleTweet)
            if(tweetScore['compound'] != 0):
                totalScore += tweetScore['compound']
                numReads +=1
        except Exception as e:
            print("couldn't score tweet: " + str(e))
        startLoc = endLoc +1
    avgSent = totalScore/numReads
    print(inputFile)
    print(avgSent)
    sentimentScores[fileIndex] = avgSent
    fileIndex +=1

# once done with calculating sentiment for all weeks in a year, write the results out to a csv file
outputFile = open(parentFolder + "/sentimentScores.csv",'w')
outputFile.write("sentimentScores \n")
index = 0
for score in sentimentScores:
    outputFile.write(str(weekNums[index]))
    outputFile.write(",")
    outputFile.write(str(score))
    outputFile.write("\n")
    index +=1
outputFile.close()



###### end of Vader.py ########