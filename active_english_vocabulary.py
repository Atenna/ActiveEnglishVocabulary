import sys
import json
import re

from Tkinter import *

# python frequency.py output3.txt | cut -d" " -f2,1 | sort -nrk2 > relative_frequency.txt && cat # relative_frequency.txt -n| head -n30
# will print top 30 most used words in English tweets
# http://www.talkenglish.com/Vocabulary/Top-2000-Vocabulary.aspx compare

tweet_file = 0
unknown = 0
sum_words = 0

def process_data():
    """Convert Twitter stream into dictionary of word - frequency pair"""
    global unknown
    global sum_words
    global unknown
    # initialize a dictionary for new unknown words
    unknown = {} 
    sum_words = 0

    # loop over the file with tweets
    for tweet in tweet_file: 
        # parse the line of tweet into json format dictionary
        dic = json.loads(tweet) 
        # coef = calculate_sentiment(tweet) - not used now
        # check for language
        if 'text' in dic.keys() and dic['lang'] == 'en': 
            textp = dic['text']
            # split the tweet by spaces
            sentence = textp.split(' ') 
 	    for word in sentence:
       	        word = word.lower() 
	        word = re.sub('[^a-z]', "", word)	
                # increment absolute amount of this term
                sum_words = sum_words + 1 
       	        unknown[word] = unknown.get(word, 0) + 1

    for key, value in unknown.items():
        if (isinstance(value, int) and 
            len(key) != 0 and key != "\n" and 
            key != " " and value != None):
            print key.encode('utf8'), (value/(sum_words*(0.0005)))

def lines(fp):
    print str(len(fp.readlines()))

def write_to_file():
    """Loop over dictionary sorted by frequency and write to file"""
    text_file = open("absolute_frequency.txt","w")
    d_view = [(v,k) for k,v in unknown.iteritems()]
    d_view.sort(reverse=True)
    for v,k in d_view:
        if k != "":
	    text_file.write("%s: %d \t" % (k,v))
	    text_file.write("http://slovnik.azet.sk/preklad/anglicko-slovensky/?q="+k)
	    text_file.write("\n")
    text_file.close()

def calculate_sentiment(tweet):
    """Method to calculate sentiment of a tweet"""
    dic = json.loads(tweet)
    coef = 0
    if 'text' in dic.keys():
        textp = dic['text']
        sentence = textp.split(" ")
        for word in sentence:
	    word = word.lower()	
	
	    if word in scores: 
	        coef = coef + scores.get(word, 0)
    return coef

def gui():
    """User interface function"""
    root = Tk() # create the window
    root.title("Frequency of English Words Used on Twitter")
    root.geometry("500x300")
    app = Frame(root); # creates a frame for widgets
    label = Label(app, text = "n words most used in English vocabulary")
    app.grid() # to make app visible
    label.grid()
    button1 = Button(app, text = "Find")
    button2 = Button(app)
    button1.grid()
    button2.grid()
    button2.configure(text = "Close")
    button3 = Button(app)
    button3.grid()
    button3["text"] = "Find translations"
    root.mainloop()
def main():

    global tweet_file
    tweet_file = open(sys.argv[1])
    process_data()
    gui()
    write_to_file()

if __name__ == '__main__':
    main()
