from numpy.lib.function_base import select
import sys
import json
import re
import hyperlink_manager
import webbrowser

from Tkinter import *

# python frequency.py output3.txt | cut -d" " -f2,1 | sort -nrk2 > relative_frequency.txt && cat # relative_frequency.txt -n| head -n30
# will print top 30 most used words in English tweets
# http://www.talkenglish.com/Vocabulary/Top-2000-Vocabulary.aspx compare

tweet_file = 0
unknown = {}
sum_words = 0
url = ""
btn_dict = []

class ActiveEnglishVocabulary(Frame):

    btn_dict = unknown
    button = []
    global url
    url = "http://slovnik.azet.sk/preklad/anglicko-slovensky/?q=word"

    def __init__(self, master):
        """ Initialize the Frame. """
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create buttons for words to open their translation in browser. """
        self.button1 = Button(self, text = "See in dictionary WORD", command=self.open_url)
        self.button1.grid()

    def open_url(self):
        webbrowser.open_new(url)


def process_data():
    """Convert Twitter stream into dictionary of word - frequency pair"""
    global unknown
    #global sum_words
    # initialize a dictionary for new unknown words
    unknown = {} 
    sum_words = 0
    sentence = []

    # loop over the file with tweets
    for tweet in tweet_file: 
        # parse the line of tweet into json format dictionary
        dic = json.loads(tweet) 
        # coef = calculate_sentiment(tweet) - not used now
        # check for language
        if 'text' in dic.keys() and dic['lang'] == 'en': 
            text = dic['text']
            # split the tweet by spaces
            sentence = text.split(' ')
        for word in sentence:
            word = word.lower()
            word = re.sub('[^a-z]', "", word)
            # increment absolute amount of this term
            sum_words += 1
            unknown[word] = unknown.get(word, 0) + 1


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


def calculate_sentiment(tweet, scores):
    """Method to calculate sentiment of a tweet

        tweet is text almost in json format
        scores is dictionary of word- sentiment scores"""
    dic = json.loads(tweet)
    coef = 0
    sentence = ""
    if 'text' in dic.keys():
        textp = dic['text']
        sentence = textp.split(" ")
        for word in sentence:
            word = word.lower()
            if word in scores:
                coef = coef + scores.get(word, 0)
    return coef

if __name__ == '__main__':
#    global tweet_file
#    global unknown
    tweet_file = open(sys.argv[1])
    process_data()
    write_to_file()
    root = Tk()
    root.title("Active English Vocabulary")
    root.geometry("500x500")
    app = ActiveEnglishVocabulary(root)
    root.mainloop()
