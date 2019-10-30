from scrap import Twitter, Reddit, Facebook
from scrap.tools import to_csv
from scrap.tools import flatten
import csv
import numpy

twt = Twitter(api_key="your_api", api_secret="your_api_secret", access_token="your-access_token",
    access_token_secret="your-access_token_secret")

tweets = twt.search("apple", count=500, exclude_replies=True,
    include_retweets=False)

result = []
for tweet in tweets:
    result.append(tweet['full_text'])

a = numpy.array(result)
# print(a)
numpy.savetxt('demo.csv', a, fmt='%s')
