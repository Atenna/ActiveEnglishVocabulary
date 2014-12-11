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
        self.button1 = Button(self, text = "Online AEV Dictionary", command=self.open_url)
        self.button1.grid()

    def open_url(self):
        webbrowser.open_new(url)



class QuitButton(Button):
    """Button for exiting the application"""
    def __init__(self, parent):
        Button.__init__(self, parent)
        # Change the message here
        self['text'] = 'See you later!'
        # Command to close the window (the destory method)
        self['command'] = parent.destroy
        self.grid()


class AboutButton(Button):
    """Button redirecting new tab to my GitHub"""
    def __init__(self, parent):
        Button.__init__(self, parent)
        self['text'] = 'Take me to the source code'
        self['command'] = self.open_about_page
        self.grid()

    def open_about_page(self):
        webbrowser.open_new("https://github.com/Atenna/ActiveEnglishVocabulary")

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
    html_file = open("absolute_frequency.html", "w")
    d_view = [(v,k) for k,v in unknown.iteritems()]
    d_view.sort(reverse=True)
    html_file.write("<ul>\n")
    for v,k in d_view:
        if k != "":
            html_file.write("<li> %s: %d \t" % (k,v))
            text_file.write("%s: %d \t" % (k,v))
            html_file.write("<a href='http://slovnik.azet.sk/preklad/anglicko-slovensky/?q="+k+"'Slovnik</a></li>\n")
            text_file.write("http://slovnik.azet.sk/preklad/anglicko-slovensky/?q="+k+"\n")
    html_file.write("</ul>")
    text_file.close()
    html_file.close()


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
    root.title("AEV")
    root.geometry("192x100")
    app = ActiveEnglishVocabulary(root)
    AboutButton(root)
    QuitButton(root)
    root.mainloop()
