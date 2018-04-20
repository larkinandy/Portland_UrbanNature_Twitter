#calcWordAssociatons.py
# created by Andrew Larkin
# for Scoial Media Analytics course project
# April 18, 2018

# This script calculates the frequency that words of interest are associated with keywords used during the Twitter search.
# Input files are part of speech tags and associations created by the Stanford NLP lexicon parser



##################### setup ########################


# import modules and perform setup
import numpy as np
import nltk as nt
import os
stemmer = nt.SnowballStemmer("english")

# Keywords used to select tweets to download.  Also used to determine which topics are grammatically related to green space
KEYWORDS_SINGULAR = ['park','tree','natur','bush','grass','flower','plant','garden','yard','backyard','leaf','forest','trail','mountain',
                     'lawn','field','crop','hay','prarie','pasture','lake','river','riverside','stream','branch']

# create stem for each keyword
for i in range(0,len(KEYWORDS_SINGULAR)):
    KEYWORDS_SINGULAR[i] = stemmer.stem(KEYWORDS_SINGULAR[i])

    
# file paths
parentFolder = "Full folder filepath"
inputFolder = parentFolder + "name of input folder"
outputFile = parentFolder + "name of file containing results"

# topics.  Each array contains list of keywords related to a specific greenspace pathway
exerciseKeys = ['hike' ,'walk','play','run','hike','play','walk','run','exercis','bik','triathlon','yoga','rac','skat','swim','jog']
aestheticKeys = ['view','sunset','green','beaut','gorgeous','look','stunning']
safetyKeys = ['crim','weapon','body','police','cop','flood','warn','knife','steal','danger','stole','kill','attack','gun','safe']
attentionKeys = ['relax','recharge','brain','stress','get a break','take a break','rest']
socialKeys = ['family','freind','join us','fest', 'jam','concert','protest','parade','march','bbq','party']
keywords = exerciseKeys + aestheticKeys + safetyKeys + attentionKeys + socialKeys

# arrays that store word frequency 
allList = []            # all words found in the input file, including stopwords
allCounts = []          # word frequency for all words in allList



################## helper functions ###############

# process single topic-keyword association (e.g. hike-park) from tagged speech file
# Each line contains three essential words - two words from the original tweet text, and the grammatical relation (e.g. 'adj') 
# between the words
# INPUTS:
#    inLine (string) - single line of text containing keywords and grammatical relation between them.  From the Stanford NLP Parser
# OUTPUTS:
#    relation (custom class) - custom class object representing the grammatical relation between variables in the input argument
def processLine(inLine):
    vals = ["a"]*3                      
    endChars = ["(","-","-"]            # chars that an association may end with
    startChars = ["("," ",","]          # chars that an association may stat with
    startIndex = 0                      # index of the first character in a topic or keyword


    # for each word in the line, extract the word from line and store in array
    for i in range(0,3) :
        endIndex = inLine.find(endChars[i],startIndex)
        vals[i] = inLine[startIndex:endIndex]
        startIndex = inLine.find(startChars[i],endIndex) + 1
    # reduce words to their grammatical stem
    vals[2] = stemmer.stem(vals[2]).lower()
    vals[1] = stemmer.stem(vals[1]).lower()
    
    # identify which urban nautre keyword is in the line and adjust counters
    for keyword in KEYWORDS_SINGULAR:
        if(keyword in vals[2].lower() or keyword in vals[1].lower()): 
            print("true")
            if(vals[2] in allList):
                allCounts[allList.index(vals[2])]+=1
            else:
                allList.append(vals[2])
                allCounts.append(1)
            if(vals[1] in allList):
                allCounts[allList.index(vals[1])]+=1
            else:
                allList.append(vals[1])
                allCounts.append(1)   
    # identify the grammatical relation between keywords.  Create relation
    tempRelation = relation(vals[1].lower(),vals[2].lower(),vals[0].lower())    
    return(tempRelation)

# read input file and calculate word frequencies
# INPUTS: 
#    filename (string) - full filepath including name of input file
# OUTPUTS:
#    sentList (class) - instance of the custom sentenceType class
def readFile(filename):
    sentNum = 0
    fStream = open(filename,'r',encoding='utf8')
    tempData = fStream.readline()
    stillData = True
    needList = True
    needSentence = True
    
    # one line for each grammatical relation.  Transform line into sentenceType class object.
    while(tempData not in [""]):
        sentNum+=1
        tempRelation = processLine(tempData)
        if(needSentence):
            tempSentence = sentenceType(tempRelation)
            needSentence = False
        else:
            tempSentence.addRelation(tempRelation)
        if(needList == True):
            sentList = sentenceList(tempSentence)
            needList = False
        else:
            sentList.addSentence(tempSentence)
        tempData = fStream.readline()
    return(sentList)


# custom class for part of speech word associations.  Stores both words and association label
class relation:
    # create a word relation
    def __init__(self,inWord1,inWord2='NaN',inType='NaN'):
        self.word1 = inWord1
        self.word2 = inWord2
        self.valType = inType

    # word1 and word2 are the two words in a grammatical relation
    
    def getWord1(self):
        return self.word1

    def getWord2(self):
        return self.word2

    # grammatical type 

    def getValType(self):
        return self.valType

# all text in a tweet.  
class sentenceType:
    # instantiate a hotspot
    def __init__(self,inRelation):
        self.relationList = []
        self.relationList.append(inRelation)
        self.wordList = []
        self.wordList.append(inRelation.getWord1())
        self.wordList.append(inRelation.getWord2())
        self.numRelations = 1

    def getRelation(self,index):
        return(self.relationList[index])

    def addRelation(self,inRelation):
        self.relationList.append(inRelation)
        if(inRelation.getWord1() not in self.wordList):
            self.wordList.append(inRelation.getWord1())
        if(inRelation.getWord2() not in self.wordList):
            self.wordList.append(inRelation.getWord2())
        self.numRelations +=1

    def getWordList(self):
        return self.wordList

    def getNumRelations(self):
        return(self.numRelations)

# a collection of sentenceType objects.  
class sentenceList:

    def __init__(self,inSentence):
        self.sentenceList = []
        self.sentenceList.append(inSentence)

    def addSentence(self,inSentence):
        self.sentenceList.append(inSentence)

    def getSentence(self,index):
        return self.sentenceList[index]

    # get keyword class object 
    # INPUTS:
    #    keyword (string) - name of the keyword, typically the lowercase characters of the keyword
    #    personalLimit (int) - maximum number of returns.  Useful for debugging
    #    allWords (boolean) - whether to include all words, including stop words
    # OUTPUTS:
    #    tempSentenceList (sentenceList) - sentenceList class containing sentenceTypes
    def getRelationsWithKeyword(self,keyword,personalLimit=0,allWords=False):
        tempList = self.getSentenceWithKeyword(keyword,personalLimit,allWords)
        tempRelationList = []
        for index in range(0,len(tempList)):
            tempSentence = tempList[index]
            for j in range(0,tempSentence.getNumRelations()):
                tempRelation = tempSentence.getRelation(j)
                if(tempRelation.getWord1() in keyword or tempRelation.getWord2() in keyword):
                    tempRelationList.append(tempRelation)
        return(tempRelationList)

    # get all sentences containing keyword of interest
    # INPUTS:
    #    keyword (array) - list of keywords used to screen for tweets of interest
    #    personalLimit (int) - max number of sentences to return
    #    allWords (boolean) - whether to include all words related to a keyword
    # OUTPUTS:
    #    tempSentenceList (sentenceList) - sentenceList class containing sentence types
    def getSentenceWithKeyword(self,keyword,personalLimit,allWords=False):
        tempList = []
        tempSentenceList = []
        for index in range(0,len(self.sentenceList)):
            tempSentence = self.sentenceList[index]
            if(allWords == True):
                foundWord = False
                for index in range(0,len(KEYWORDS_PLURAL)):
                    if(not foundWord):
                        if(KEYWORDS_PLURAL[index] in tempSentence.getWordList() or KEYWORDS_SINGULAR[index] in tempSentence.getWordList()):
                            if(tempSentence.getPersonal() >= personalLimit):
                                tempSentenceList.append(tempSentence)
                                foundWord = True
            else:
                if(keyword[0] in tempSentence.getWordList() or keyword[1] in tempSentence.getWordList()):
                    if(tempSentence.getPersonal() >= personalLimit):
                        tempSentenceList.append(tempSentence)

        return(tempSentenceList)

# keywords used during Twitter search
class keyWord:
    def __init__(self,inKeyWord,inSentList,personalLimit,allVals=False):
        self.keyWord = inKeyWord
        self.relationList = inSentList.getRelationsWithKeyword(inKeyWord,personalLimit,allVals)
        self.tempWordList = []
        self.wordFreq = []
        self.setWordFreq()

    def getKeyword(self):
        return self.keyWord

    def setKeyword(self,inKeyword):
        self.keyWord = inKeyword

    def getWordFreq(self):
        return self.wordFreq

    def getWordList(self):
        return self.tempWordList

    def getSampSize(self):
        return self.numSentences


def main():

    # setup output file with head and iteratively write output for each loop
    fStream = open(outputFile,'w')
    for varName in keywords:
        fStream.write(varName)
        fStream.write(',')
    fStream.write('\n')

    inputFiles = os.listdir(inputFolder)
    # one file for each weeks worth of tweets
    for inputFile in inputFiles:   
        keyCounts = [0]*len(keywords)
        parserFile = inputFolder + inputFile
        sentList = readFile(parserFile)
        #sentList.screenForSentiment('human',-1)
        index = 0
        for keyword in keywords:
            if(keyword in allList):
                tempIndex = allList.index(keyword)
                keyCounts[index] = allCounts[tempIndex]  -  keyCounts[index] 
                allCounts[tempIndex] = 0#keyCounts[index] 
                fStream.write(str(keyCounts[index]))
            else:
                fStream.write('0')
            fStream.write(',')
            index +=1
        fStream.write('\n')

    fStream.close()

    print(keyCounts)
    print("completed main function")

# end of calcWordAssociations_v2.py

main()