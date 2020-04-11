#import sys
#import os
#import string
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
from ta_functions import *


#Startup checks
#######################################################################################################
# Check that an argument was entered at the command line (name of log file to be looked at).
# Check if file exists.
#######################################################################################################
fileTest()  #make sure file entered by user does exist and accessible.


#passed checks good to go.
#######################################################################################################
# Global Variables
#######################################################################################################
text_file_name= sys.argv[1]
stop_word_file_name = "stop_words.txt"
line_num = 0
count = 0
pos = 0.0
neg = 0.0
neu = 0.0
mostPositive = 0.0
mostNegative = 0.0
mostPos = ""
mostNeg = ""
sentCount = 0
main_list = []
words = []
words2 = []
words3 = []
links = []
hashtags = []
stop_words = []
processWordList = []


#load stop words into list
stop_words = load_stop_words(stop_word_file_name)

#open file to be analyzed
log_file = open(text_file_name, "r")
    
#Parse each line, take what we need and then discard
for line in log_file:
    sentiment = [] 
    line_num += 1
    words = line.split()                                    #Each word becomes a list item
    if words[1] == "-!-":
        continue
    
    sentCount = sentCount + 1
    sentiment = calcSentiment(line)                         #calcSentiment returns a list of doubles for each sentence
    pos = pos + sentiment[0]                                #[positive, negative, neutral]
    neg = neg + sentiment[1]
    neu = neu + sentiment[2]

#find the most positive and most negative line in the log
    if sentiment[0] > sentiment[1] and sentiment[0] > mostPositive:
        mostPositive = sentiment[0]
        mostPos = line
    
    if sentiment[1] > sentiment[0] and sentiment[1] > mostNegative:
        mostNegative = sentiment[1]
        mostNeg = line
    
    words = words[4: ]                                      #list slice removing the 1st three elements (time, <, and nickname)
    words2 = [ word.strip("<>,.;:!?\[]^1234567890\"@ ") for word in words ]   #New list strips useless stuff from both ends
   
#Function is non destructive to the line - looks for hashtags, links, and words                       
    processWordList = processList(words2, stop_words)  
    for word in processWordList[0]:
        main_list.append(word)
    for link in processWordList[1]:
        links.append(link)
    for hashTag in processWordList[2]:
        hashtags.append(hashTag)
    
#TODO add function to gather n-grams
#End For loop
#######################################################################################################


#At this point there is a list of internet links.  Next function writes them to an HTML file so user
#can easily open and click on them instead of copy/paste.
processLinks(links, pos, neg, neu, sentCount)
    
processHashTags(hashtags, pos, neg, neu, sentCount)
    
countWords(main_list, pos, neg, neu, sentCount)

log_file.close()

finalPos = "{0:.1f}%".format(((pos/sentCount)* 100))
print("Processed {} lines".format(line_num))
print("processed {} words".format(len(main_list)))
print("Processed {} links".format(len(links)))
print("Processed {} hashtags".format(len(hashtags)))
print("Sentiment count: " + str(sentCount) + "\n")
print("AVG Sentiment positive: " + "{0:.1f}%".format(((pos/sentCount)* 100)))
print("AVG Sentiment negative: " + "{0:.1f}%".format(((neg/sentCount)* 100)))
print("AVG Sentiment neutral: " + "{0:.1f}%".format(((neu/sentCount)* 100)))
print("Most positive line: " + mostPos)
print("Most negative line: " + mostNeg)

#/home/medukonis/irc/freenode/##truth.2020-04-11.log
