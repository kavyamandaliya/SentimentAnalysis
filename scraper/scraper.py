from scrap import Twitter, Reddit, Facebook
from scrap.tools import to_csv
from scrap.tools import flatten

twt = Twitter(api_key="Tr0lCgQ0oI3Bk9RerYVAycIt4", api_secret="Y73LCeFrfmOPgPMZR4eTfTw09mowFrV1SfO3xq53ckhWQVzxdS", access_token="1177103933883305984-QF7k3lonC9v1ae3I46rTtcoeCSHxKu",
    access_token_secret="Fjrna4ekfX3ysYvSJWKWJUEHxdpAccf1A256WwTTefJgM")

tweets = twt.search("Happy Diwali", count=500, exclude_replies=True,
    include_retweets=False)

result = []
for tweet in tweets:
    result.append(tweet['full_text'])

for r in result:
    print(r + "\n")   

# rdt = Reddit("Ai6JXhZ3M5hGQA", "YnpYuFmTkdJWb4nbwV8FB3Nwds4")
#
# comments = rdt.search("pizza", count=50, order="new", page='',
#     result_type="link", time_period="all")
#
# # Convert nested dictionary into flat dictionary
# comments = [flatten(comment) for comment in comments]

# Sort by comment score
# comments = sorted(comments, key=lambda k: k['data.score'], reverse=True)

# Print the top 10
# for comment in comments[:9]:
#     print("###\nUser: {}\nScore: {}\nComment: {}\n".format(comment['data.author'], comment['data.score'], comment['data.body']))

# fbk = Facebook("800ab00690b75ddd1e0eee30dae9038e")
#
# comments = fbk.page_posts_comments("mcdonalds", post_count=1000,
#     comment_count=100000)
#
# for comment in comments:
#     print(comment['message'])
