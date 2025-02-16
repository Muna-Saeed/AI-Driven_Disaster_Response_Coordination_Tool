import tweepy
import json

# Set up Twitter API credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAF22ywEAAAAA0r315os3QKKD62T1lKvxlFRGqbg%3D59xZ21XKnjP1HKcbR5dsbGo9Ieh3JUIvRYvsKM6mWKRQZfqsl9"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Define search query for disaster-related tweets
query = "(earthquake OR flood OR fire OR hurricane OR rescue) -is:retweet lang:en"

# Fetch recent tweets
tweets = client.search_recent_tweets(query=query, max_results=100, tweet_fields=["created_at", "text", "geo"])

# Process and store tweets
for tweet in tweets.data:
    print(f"Time: {tweet.created_at}, Tweet: {tweet.text}")
