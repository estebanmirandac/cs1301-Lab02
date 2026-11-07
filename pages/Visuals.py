# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
with open("data.json") as f:             
    data = json.load(f)                   

st.subheader(data["chart_title"])         

df = pd.DataFrame(data["data_points"])    
st.header("Wins per Golfer")
st.write("This bar chart shows how many PGA Tour wins each golfer has in the 2026 season.")
st.bar_chart(df, x="golfer", y="wins")

st.header("Distance vs. Accuracy")
st.write("Compares golfers average driving distance with how accurate they are on landing in the fairway")

st.slider(
    "Minimum wins",
    min_value=0,
    max_value=int(df["wins"].max()),
    key="min_wins"
)
filtered = df[df["wins"] >= st.session_state.min_wins]


fig = px.scatter(
    filtered,
    x="driving_distance",
    y="driving_accuracy",
    hover_name="golfer",
    title="Driving Distance vs. Driving Accuracy (2026)",
    labels={
        "driving_distance": "Driving Distance (yards)",
        "driving_accuracy": "Driving Accuracy (%)"
    }
)
st.plotly_chart(fig)

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
csv_df = pd.read_csv("data.csv")
st.header("Favorite PGA Tour Golfers")
st.write("This pie chart shows which golfers people picked as their favorite in the survey.")

pie = px.pie(
    csv_df,
    names="Category",
    title="Survey Results: Favorite PGA Tour Golfer"
    
st.plotly_chart(pie)

st.header("Average Rounds per Month by Favorite Golfer")
st.write("Pick golfers to compare how many rounds per month their fans play on average.")

st.multiselect(
    "Pick golfers to compare",
    csv_df["Category"].unique(),
    default=csv_df["Category"].unique(),
    key="picked_golfers"
)

filtered_csv = csv_df[csv_df["Category"].isin(st.session_state.picked_golfers)]

avg_rounds = filtered_csv.groupby("Category")["Value"].mean()
st.bar_chart(avg_rounds)
