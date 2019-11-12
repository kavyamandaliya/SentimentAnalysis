from textblob import TextBlob
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')

keyword = ""
filePath = "scraper/" + keyword + ".csv"
filePathRecent = "scraper/" + keyword + "Recent.csv"
# text1 = 'I am very irritated, cause the code is not working, and it is giving several errors. The movie was a total waste of time. And it went on for so long that I got bored'
# sum1 = TextBlob(text1)
# sent1 = sum1.sentiment.polarity
# print(sent1)

def getSentiments(txt):
    positive = 0
    negative = 0
    neutral = 0
    print(len(texts))
    for t in texts:
        #     print(t)
        sentiment = sid.polarity_scores(t)
        for k in sorted(sentiment):
            if sentiment[k] > 0:
                positive += 1
            if sentiment[k] < 0:
                negative += 1
            if sentiment[k] == 0.0:
                neutral += 1
    print("Negative: " + str(negative))
    print("Positive: " + str(positive))
    print("Neutral: " + str(neutral))


####### MAIN FUNCTION ##########
sid = SentimentIntensityAnalyzer()
import nltk
data = pd.read_csv(filePath, header=None,error_bad_lines=False,quotechar=None, quoting=3)
dataRecent = pd.read_csv(filePathRecent,header=None,error_bad_lines=False,quotechar=None, quoting=3)
texts = data[0]
textsRecent = dataRecent[0]
getSentiments(texts)
getSentiments(textsRecent)
