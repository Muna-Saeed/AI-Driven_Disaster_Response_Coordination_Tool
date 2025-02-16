import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import tweepy

# Download stopwords
nltk.download('stopwords')
nltk.download('punkt')

# Twitter API setup (Replace with your keys)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAF22ywEAAAAA0r315os3QKKD62T1lKvxlFRGqbg%3D59xZ21XKnjP1HKcbR5dsbGo9Ieh3JUIvRYvsKM6mWKRQZfqsl9"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Fetch raw tweets
query = "(earthquake OR flood OR fire OR hurricane OR rescue) -is:retweet lang:en"
tweets = client.search_recent_tweets(query=query, max_results=100, tweet_fields=["created_at", "text", "geo"])

def clean_tweet(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove links
    text = re.sub(r"@\w+|\#", "", text)  # Remove mentions & hashtags
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)  # Remove special characters
    words = word_tokenize(text.lower())  # Tokenization & lowercasing
    words = [word for word in words if word not in stopwords.words("english")]  # Remove stopwords
    return " ".join(words)

# Process tweets
cleaned_tweets = []
for tweet in tweets.data:
    cleaned_tweets.append({"Time": tweet.created_at, "Cleaned_Tweet": clean_tweet(tweet.text), "Geo": tweet.geo})

df_tweets = pd.DataFrame(cleaned_tweets)
print(df_tweets.head())

df_tweets.to_csv("cleaned_tweets.csv", index=False)

