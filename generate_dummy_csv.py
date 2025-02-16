import pandas as pd

# Example data for sentiment analysis
data = {
    "Sentiment": ["Positive", "Negative", "Neutral", "Positive", "Negative"]
}

df = pd.DataFrame(data)

# Save to CSV
df.to_csv("analyzed_tweets.csv", index=False)

