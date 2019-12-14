from scrap import Twitter, Reddit, Facebook
from scrap.tools import to_csv
from scrap.tools import flatten
import csv
import numpy

keyword = "Iphone"
csvName = keyword + ".csv"
csvNewName = keyword + "Recent.csv"
twt = ""
rdt = ""

##BLURRED OUT THE API KEYS FOR PRIVACY CONCERNS 
def getInitData(fileName):
    twt = Twitter(api_key="XXX", api_secret="XXX",
                  access_token="XXX",
                  access_token_secret="XXX")
    rdt = Reddit("XXX", "XXX")
    ##twitter
    tweets = twt.search(keyword, count=500, exclude_replies=True,
        include_retweets=False)
    result = []
    for tweet in tweets:
        result.append(tweet['full_text'])
    ##reddit
    comments = rdt.search(keyword, count=20000, order="new", page='',
        result_type="link", time_period="year")
    comments = [flatten(comment) for comment in comments]
    comments = sorted(comments, key=lambda k: k['data.score'], reverse=True)
    for comment in comments:
        result.append(comment['data.selftext'])
    a = numpy.array(result)
    # print(a)
    numpy.savetxt(fileName, a, fmt='%s')

def getNewData(fileName):
    twt = Twitter(api_key="XXX", api_secret="XXX",
                  access_token="XXX",
                  access_token_secret="XXX")
    rdt = Reddit("XXX", "XXX")
    ##twitter
    tweets = twt.search(keyword, count=500, exclude_replies=True,
        include_retweets=False)
    result = []
    for tweet in tweets:
        result.append(tweet['full_text'])
    ##reddit
    comments = rdt.search(keyword, count=20000, order="new", page='',
        result_type="link", time_period="month")
    comments = [flatten(comment) for comment in comments]
    for comment in comments:
        result.append(comment['data.selftext'])
    a = numpy.array(result)
    # print(a)
    numpy.savetxt(fileName, a, fmt='%s')

#####   MAIN METHOD  ######
getInitData(csvName)
getNewData(csvNewName)
