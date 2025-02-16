import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
df_tweets = pd.read_csv("analyzed_tweets.csv")
df_weather = pd.read_csv("cleaned_weather_data.csv")
df_disaster = pd.read_csv("classified_disasters.csv")

st.title("Disaster Insights Dashboard")

# Tweet Sentiment Analysis
st.subheader("Tweet Sentiment Analysis")
sentiment_counts = df_tweets["Sentiment"].value_counts()
fig = px.pie(names=sentiment_counts.index, values=sentiment_counts.values, title="Sentiment Distribution")
st.plotly_chart(fig)

# Disaster Image Classification
st.subheader("Disaster Zones")
st.image("assets/disaster_zones.png", caption="Disaster zones classified from satellite images.")
disaster_fig = px.bar(df_disaster, x="Type", y="Count", title="Disaster Type Detection", color="Type")
st.plotly_chart(disaster_fig)

# Weather Prediction and Severity
st.subheader("Disaster Severity Prediction")
disaster_type = st.selectbox("Filter by Disaster Type", df_weather["Disaster Type"].unique())
filtered_data = df_weather[df_weather["Disaster Type"] == disaster_type]
severity_fig = px.line(filtered_data, x="Timestamp", y="Disaster Severity", title=f"Disaster Severity Trend for {disaster_type}", markers=True)
st.plotly_chart(severity_fig)

