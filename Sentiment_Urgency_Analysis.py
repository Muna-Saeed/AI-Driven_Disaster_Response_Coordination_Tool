import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Download sentiment tools
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
print(sia.polarity_scores("This is a test tweet"))

# Load cleaned tweets
df_tweets = pd.read_csv("cleaned_tweets.csv")
print(df_tweets.head())

# Function to classify sentiment
def classify_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment classification
df_tweets["Sentiment"] = df_tweets["Cleaned_Tweet"].apply(classify_sentiment)

# Urgency detection using a BERT-based model
urgency_classifier = pipeline("text-classification", model="facebook/bart-large-mnli")
print(urgency_classifier("This is an urgent rescue operation."))


def detect_urgency(text):
    result = urgency_classifier(text)
    labels = {label["label"]: label["score"] for label in result}
    return "Urgent" if labels.get("ENTAILMENT", 0) > 0.8 else "Non-Urgent"

# Apply urgency detection
df_tweets["Urgency"] = df_tweets["Cleaned_Tweet"].apply(detect_urgency)

# Display results
print(df_tweets.head())

# Save processed data
df_tweets.to_csv("analyzed_tweets.csv", index=False)
