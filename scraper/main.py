from socialreaper import Twitter
from socialreaper.tools import to_csv

twt = Twitter(api_key="your_api", api_secret="your_api_secret", access_token="your-access_token",
    access_token_secret="your-access_token_secret")

tweets = twt.search("apple", count=500, exclude_replies=True,
    include_retweets=False)

to_csv(list(tweets), filename='apple.csv')
