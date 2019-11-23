from scrap import Twitter, Reddit, Facebook
from scrap.tools import to_csv
from scrap.tools import flatten
import csv
import numpy

keyword = "Dominos"
csvName = keyword + ".csv"
csvNewName = keyword + "Recent.csv"
twt = ""
rdt = ""

def getInitData(time, fileName):
    twt = Twitter(api_key="Tr0lCgQ0oI3Bk9RerYVAycIt4", api_secret="Y73LCeFrfmOPgPMZR4eTfTw09mowFrV1SfO3xq53ckhWQVzxdS",
                  access_token="1177103933883305984-QF7k3lonC9v1ae3I46rTtcoeCSHxKu",
                  access_token_secret="Fjrna4ekfX3ysYvSJWKWJUEHxdpAccf1A256WwTTefJgM")
    rdt = Reddit("Ai6JXhZ3M5hGQA", "YnpYuFmTkdJWb4nbwV8FB3Nwds4")
    ##twitter
    tweets = twt.search(keyword, count=500, exclude_replies=True,
        include_retweets=False)
    result = []
    # for tweet in tweets:
    #     result.append(tweet['full_text'])
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
getInitData("year", csvName)
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