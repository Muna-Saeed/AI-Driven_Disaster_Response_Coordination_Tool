import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import pickle
import os

# Initialize Dash app
app = dash.Dash(__name__)

# Load datasets
df_tweets = pd.read_csv("analyzed_tweets.csv")  # Sentiment analysis results
df_weather = pd.read_csv("cleaned_weather_data.csv")  # Weather data for severity trends
df_disaster = pd.read_csv("classified_disasters.csv")  # Dynamically generated from classification script

# Load disaster severity prediction model
with open("disaster_severity_model.pkl", "rb") as file:
    severity_model = pickle.load(file)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Disaster Insights Dashboard", style={"textAlign": "center"}),

    # Section 1: Tweet Sentiment Analysis
    html.Div([
        html.H2("Tweet Sentiment Analysis"),
        dcc.Graph(id="sentiment-pie"),
    ]),

    # Section 2: Disaster Image Classification
    html.Div([
        html.H2("Disaster Zones"),
        html.Div([
            html.Img(src="assets/disaster_zones.png", style={"width": "80%", "margin": "auto"}),
            html.P("Disaster zones classified from satellite images.", style={"textAlign": "center"}),
        ]),
        dcc.Graph(id="disaster-bar"),
    ]),

    # Section 3: Weather Prediction and Severity
    html.Div([
        html.H2("Disaster Severity Prediction"),
        html.Label("Filter by Disaster Type:"),
        dcc.Dropdown(
            id="severity-filter",
            options=[{"label": t, "value": t} for t in df_weather["Disaster Type"].unique()],
            value=df_weather["Disaster Type"].unique()[0],
            placeholder="Select a disaster type",
        ),
        dcc.Graph(id="severity-trend"),
    ]),
])


# Callbacks for dynamic updates
@app.callback(
    Output("sentiment-pie", "figure"),
    Input("sentiment-pie", "id")
)
def update_sentiment_pie(_):
    sentiment_counts = df_tweets["Sentiment"].value_counts()
    fig = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Sentiment Distribution"
    )
    return fig


@app.callback(
    Output("disaster-bar", "figure"),
    Input("disaster-bar", "id")
)
def update_disaster_bar(_):
    fig = px.bar(
        df_disaster,
        x="Type",
        y="Count",
        title="Disaster Type Detection",
        color="Type"
    )
    return fig


@app.callback(
    Output("severity-trend", "figure"),
    [Input("severity-trend", "id"),
     Input("severity-filter", "value")]
)
def update_severity_trend(_, selected_type):
    filtered_data = df_weather[df_weather["Disaster Type"] == selected_type]
    
    # Predict disaster severity using the model (if applicable)
    if "Severity Factors" in filtered_data.columns:  # Assuming you have features for prediction
        predictions = severity_model.predict(filtered_data[["Severity Factors"]])
        filtered_data["Predicted Severity"] = predictions
    
    fig = px.line(
        filtered_data,
        x="Timestamp",
        y="Disaster Severity",  # Use "Predicted Severity" if predictions are generated
        title=f"Disaster Severity Trend for {selected_type}",
        markers=True
    )
    return fig


# Ensure disaster_zones.png exists
if not os.path.exists("assets/disaster_zones.png"):
    os.makedirs("assets", exist_ok=True)
    # Placeholder image creation (if needed)
    with open("assets/disaster_zones.png", "wb") as f:
        pass  # Save the actual image here


# Run app
if __name__ == "__main__":
   # app.run_server(debug=True)
    app.run_server(port=8051)


