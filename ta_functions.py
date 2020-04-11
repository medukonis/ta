import sys
import os
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

#######################################################################################################
# Function Definitions
#######################################################################################################

#######################################################################################################
# Name:     load_stop_words()
# Input:    string - file name
# Output:   list - stop words
# Usage:    Loads stop word file into a python array/list for use in analysis.
#######################################################################################################

def load_stop_words(the_stop_word_file):
    x = []          #list that will be returned
    stop_word_file = open(the_stop_word_file, "r")
    for each_word in stop_word_file:
        x.append(each_word.strip())  #removes the newline char on each
    return x


#######################################################################################################
# Name:     fileTest()
# Input:    None
# Output:   None
# Usage:    Test that logfile entered on command line does exist and accessible.  If not, exit program.
#######################################################################################################
def fileTest():
    if len(sys.argv) < 2:
        print("***** Usage: index.py 'name of log file to be analyzed *****")
        exit(0)
    else:
        try:
            test = open(sys.argv[1])
            test.close()  #happy path.  If good here, move on to rest of program.
        except IOError:
            print("File not accessible or does not exist - exiting")
            exit(0)

#######################################################################################################
# Name:     processList(word_list)
# Input:    list
# Output:   list of lists
# Usage:    Removes words less than 4 chars, removes words starting with tilde, removes words starting
#           double hashtag.  Appends hashtagged words to hashtag list, appends words starting with 
#           http to list of links, and finally, appends keeper words to a list.
#######################################################################################################
#look for links, hastags, and words we wish to count.  Pitch words we dont want.
def processList(word_list, stopWords):
    main = []
    link = []
    hasht = []
    for word in word_list:
        if len(word) > 3:
            if word.lower() in stopWords:                          #remove useless words we dont want to count
                #print("removing " + word)                          #for testing
                continue                                            #if its a match for stop word, start over at beginning of for loop
            elif word[0] == "#" and word[1] != "#":                 #single # is a hashtag - save it                         
                hasht.append(word)
                continue 
            elif word[0] =="h" and word[1] =="t" and word[2] =="t" and word[3] =="p":  
                link.append(word)                                  #http - this is a link - save it
                continue                
            else:                                                   #doesnt match any other criteria, its a keeper
                main.append(word.lower())                           #keeper - turn to all lower case 
                                                                    #and append to list for count later
    return [main, link, hasht]

#######################################################################################################
# Name:     processLinks(link_list, p, n, neut, cnt)
# Input:    list, double, double, double, integer
# Output:   None
# Usage:    Takes a list of links that are text and writes out an html file.  The doubles are positive
#           negative, and neutral sentiment numbers.  Integer is the number of lines to average by
#######################################################################################################                

def processLinks(link_list, p, n, neut, cnt):
    links = list( dict.fromkeys(link_list) )    #remove duplicates by converting to a dictionary then back to list
    filename = "results/" + sys.argv[1] + "/links.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')
    f.write("<!DOCTYPE html>\n<html>\n<body>")      
    #count number of links and write to top of file
    f.write("<p>"+ sys.argv[1] + "</p>")
    f.write("<p>processed {} links</p>".format(len(links)))
    f.write("<p>AVG Sentiment positive: " + "{0:.1f}%".format(((p/cnt)* 100))+ "<br>")
    f.write("AVG Sentiment negative: " + "{0:.1f}%".format(((n/cnt)* 100))+ "<br>")
    f.write("AVG Sentiment neutral: " + "{0:.1f}%".format(((neut/cnt)* 100))+ "</p>")
    #write each link on a seperate line
    for link in links:
        f.write("<p>" + "<a href=\'" + link + "\'>"+ link +"</a></p></br>")
    f.write("</body>\n</html>")   
    f.close()

#######################################################################################################
# Name:     processHashTags(tag_list, p, n, neut, cnt)
# Input:    list, double, double, double
# Output:   None
# Usage:    Takes a list of hashtags found in text, cleans up the list, and writes them to an HTML 
#           file.  User can open this file with browser and click on them to search twitter.  The 
#           doubles are positive, negative, and neutral sentiment numbers.
#           Integer is the number of lines to average by
#######################################################################################################
#TODO: delete dups
def processHashTags(tag_list, p, n, neut, cnt):
    #remove duplicate hashtags by converting to dictionary then back to list
    hashtags = list( dict.fromkeys(tag_list) )
    #Write hashtags to a file
    filename = "results/" + sys.argv[1] + "/hashtags.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')
    f.write("<!DOCTYPE html>\x0A<html>\x0A<body>\x0A") 
    f.write("<p>"+ sys.argv[1] + "</p>\x0A")
    #count number of hashtags and write to top of file
    f.write("<p>processed {} hashtags</p>\x0A".format(len(hashtags)))
    f.write("<p>AVG Sentiment positive: " + "{0:.1f}%".format(((p/cnt)* 100))+ "<br>")
    f.write("AVG Sentiment negative: " + "{0:.1f}%".format(((n/cnt)* 100))+ "<br>")
    f.write("AVG Sentiment neutral: " + "{0:.1f}%".format(((neut/cnt)* 100))+ "</p>")
    #write each hashtag on a seperate line
    for hashtag in hashtags:   #TODO figure out some better formatting - table? columns?
        f.write("<p>" + "Twitter: <a href=https://twitter.com/search/?q=%23"  + hashtag[1:] + ">" + hashtag +"</a>&nbsp;&nbsp;&nbsp;")
        f.write("Facebook: <a href=https://www.facebook.com/hashtag/"  + hashtag[1:] + ">" + hashtag +"</a>&nbsp;&nbsp;&nbsp;")
        f.write("Instagram: <a href=https://www.instagram.com/explore/tags/"  + hashtag[1:] + "/"+">" + hashtag +"</a></p></br>\x0A")
    f.close()
    
#Done with links and hashtags

#######################################################################################################
# Name:     countWords(main_word_list, p, n, neut, cnt)
# Input:    list, double, double, double
# Output:   None
# Usage:    TODO: fill in usage  The doubles are positive, negative, and neutral sentiment numbers.
#######################################################################################################
def countWords(main_word_list, p, n, neut, cnt):
    occurences = {}
    filename = "results/" + sys.argv[1] + "/word_count.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')
    f.write("AVG Sentiment positive: " + "{0:.1f}%".format(((p/cnt)* 100))+ "\n")
    f.write("AVG Sentiment negative: " + "{0:.1f}%".format(((n/cnt)* 100))+ "\n")
    f.write("AVG Sentiment neutral: " + "{0:.1f}%".format(((neut/cnt)* 100))+ "\n")
    for elem in main_word_list:
        count = main_word_list.count(elem)
        occurences.update({elem : count})

    #sort by most to least then write to file
    for key, value in sorted(occurences.items(), key=lambda item: item[1], reverse=True):
        f.write(key +' : ' + str(value) + "\n")
    f.close()  
    
#######################################################################################################
# Name:     calcSentiment(sentence)
# Input:    string
# Output:   List
# Usage:    TODO: fill in usage
#######################################################################################################
def calcSentiment(sentence): 
    positive = 0.0
    negative = 0.0
    neutral = 0.0
  
    # Create a SentimentIntensityAnalyzer object. 
    sid_obj = SentimentIntensityAnalyzer() 
  
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    sentiment_dict = sid_obj.polarity_scores(sentence)
    
    #For testing
    #print("Overall sentiment dictionary is : ", sentiment_dict) 
    #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative") 
    #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral") 
    #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive") 
    #print("Sentence Overall Rated As", end = " ") 

    positive = sentiment_dict['pos']
    negative = sentiment_dict['neg']
    neutral  = sentiment_dict['neu']
    
    return [positive, negative, neutral]
  
   
#End Function Definitions #############################################################################
