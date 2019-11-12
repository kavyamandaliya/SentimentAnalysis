from scrap import Twitter, Reddit, Facebook
from scrap.tools import to_csv
from scrap.tools import flatten
import csv
import numpy

keyword = "Dance"
csvName = keyword + ".csv"
csvNewName = keyword + "Recent.csv"

def getInitData(time, fileName):
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
    comments = rdt.search(keyword, count=500, order="new", page='',
                          result_type="link", time_period=time)
    comments = [flatten(comment) for comment in comments]
    comments = sorted(comments, key=lambda k: k['data.score'], reverse=True)
    for comment in comments[:500]:
        result.append(comment['data.selftext'])
    a = numpy.array(result)
    # print(a)
    numpy.savetxt(fileName, a, fmt='%s')


#####   MAIN METHOD  ######
getInitData("month", csvName)
getInitData("hour", csvNewName)

# fbk = Facebook("EAAepvVwDSngBAPdgRhZA4J60Sa7UdFdAIC4mgCKghXqTstFZBKOxERKLDSTMFo5mLCMmaxuZBpQtiAPWWZCBkvDzBtynDVKdEfZCY9mD0OGxS3nuOukXm5OUCh6sk05cmFmxCelca5x8akdMuF3DQzZAz9qrs1veqQVMK4rIili0ManT9xfmILIx5C0XxtgYXNnUAhNXeQNTgexrEjSZCU8gzLRZCpmkb6yJ1ai8ZCFTwwwZDZD")
#
# comments = fbk.page_posts_comments("mcdonalds", post_count=1000,
#     comment_count=100000)
#
# for comment in comments:
#     print(comment['message'])

# for r in result:e
#     print(r + "\n")