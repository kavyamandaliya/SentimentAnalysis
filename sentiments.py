from textblob import TextBlob
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')

# text1 = 'I am very irritated, cause the code is not working, and it is giving several errors. The movie was a total waste of time. And it went on for so long that I got bored'
# sum1 = TextBlob(text1)
# sent1 = sum1.sentiment.polarity
# print(sent1)
sid = SentimentIntensityAnalyzer()
data = pd.read_csv("scraper/demo.csv",header=None,error_bad_lines=False,quotechar=None, quoting=3)
# print(data)

texts = data[0]
positive = 0
negative = 0
neutral = 0
for t in texts:
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