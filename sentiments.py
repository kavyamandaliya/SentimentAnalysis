from textblob import TextBlob
import nltk
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.graph_objects as go
import plotly.express as px

nltk.downloader.download('vader_lexicon')

keyword = ""
filePath = "scraper/" + keyword + ".csv"
filePathRecent = "scraper/" + keyword + "2.csv"

def getInitSentiments(txt):
    global positiveI
    global negativeI
    global neutralI
    # print(len(txt))
    for t in txt:
        #     print(t)
        sentiment = sid.polarity_scores(t)
        for k in sorted(sentiment):
            if sentiment[k] > 0:
                positiveI += 1
            if sentiment[k] < 0:
                negativeI += 1
            if sentiment[k] == 0.0:
                neutralI += 1

def getLastSentiments(txt):
    global positiveR
    global negativeR
    global neutralR
    print(len(txt))
    for t in txt:
        #     print(t)
        sentiment = sid.polarity_scores(t)
        for k in sorted(sentiment):
            if sentiment[k] > 0:
                positiveR += 1
            if sentiment[k] < 0:
                negativeR += 1
            if sentiment[k] == 0.0:
                neutralR += 1

# def makeGraph():


####### MAIN FUNCTION ##########
sid = SentimentIntensityAnalyzer()
data = pd.read_csv("scraper/Dance.csv",header=None,error_bad_lines=False,quotechar=None, quoting=3)
dataRecent = pd.read_csv("scraper/Dance2.csv",header=None,error_bad_lines=False,quotechar=None, quoting=3)
texts = data[0]
textsRecent = dataRecent[0]
positiveI = 0
negativeI = 0
neutralI = 0
positiveR = 0
negativeR = 0
neutralR = 0
getInitSentiments(texts)
getLastSentiments(textsRecent)
positive = [0 ,0]
negative = [0, 0]
neutral = [0, 0]
positive[0] = positiveI
negative[0] = negativeI
neutral[0] = neutralI
positive[1] = positiveR
negative[1] = negativeR
neutral[1] = neutralR
# print(negative)
# print(neutral)
# print(positive)



x = np.arange(3)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=negative,
                    mode='lines+markers',name='NEGATIVE'))
fig.add_trace(go.Scatter(x=x, y=positive,
                    mode='lines+markers',name='POSITIVE'))
fig.add_trace(go.Scatter(x=x, y=neutral,
                    mode='markers+lines', name='NEUTRAL'))

fig.show()

