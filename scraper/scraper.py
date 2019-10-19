from scrap import Twitter
from scrap.tools import to_csv

twt = Twitter(api_key="Tr0lCgQ0oI3Bk9RerYVAycIt4", api_secret="Y73LCeFrfmOPgPMZR4eTfTw09mowFrV1SfO3xq53ckhWQVzxdS", access_token="1177103933883305984-QF7k3lonC9v1ae3I46rTtcoeCSHxKu",
    access_token_secret="Fjrna4ekfX3ysYvSJWKWJUEHxdpAccf1A256WwTTefJgM")

tweets = twt.search("apple", count=500, exclude_replies=True,
    include_retweets=False)

to_csv(list(tweets), filename='apple.csv')
