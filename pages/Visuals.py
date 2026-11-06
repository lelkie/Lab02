# This creates the page for displaying data visualizations.
import json
import pandas as pd
import streamlit as st
import plotly.express as px
# all data sourced from albumoftheyear.org, 2026
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json") as f:
    data = json.load(f)
df = pd.DataFrame(data["data_points"])

#static chart (plotly bar)
st.header("All Albums by Critic Score")
fig = px.bar(
    df,
    x="label",
    y="value",
    hover_data=["artist"],
    title=data["chart_title"],
    labels={"label": "Album", "value": "Critic Score", "artist": "Artist"},
)
st.plotly_chart(fig)

#dynamic chart ( line chart with slider)
st.header("Top Albums")

if "top_n" not in st.session_state:
    st.session_state.top_n = len(df)

st.session_state.top_n = st.slider(
    "Number of albums to show:",
    min_value=2,
    max_value=len(df),
    value=st.session_state.top_n,
)

shown = df.head(st.session_state.top_n)
st.line_chart(shown.set_index("label")["value"])
st.table(shown[["label", "artist", "value"]].rename(
    columns={"label": "Album", "artist": "Artist", "value": "Critic Score"}
))

#extra credit (displays mean and median of data)
mean1 = shown["value"].mean()
median1 = shown["value"].median()

if "prev_mean1" not in st.session_state:
    st.session_state.prev_mean1 = mean1
    st.session_state.prev_median1 = median1

col1, col2 = st.columns(2)
col1.metric("Mean score", round(mean1, 1), delta = round(mean1 - st.session_state.prev_mean1, 1))
col2.metric("Median score", median1, delta = median1 - st.session_state.prev_median1)

st.session_state.prev_mean1 = mean1
st.session_state.prev_median1 = median1
# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
csv_df = pd.read_csv("data.csv")

#static pie chart (plotly pie)
st.header("Survey Ratings Breakdown")
pie = px.pie(
    csv_df,
    names = "album",
    values = "rating",
    title = "Share of Total Rating by Album",
)
st.plotly_chart(pie)

#dynamic chart ( bar chart with a slider)
st.header("Survey Ratings by Album")
if "min_rating" not in st.session_state:
    st.session_state.min_rating = 1

st.session_state.min_rating = st.slider(
    "Minimum rating to show:",
    min_value = 1,
    max_value = 10,
    value = st.session_state.min_rating,
)

filtered = csv_df[csv_df["rating"] >= st.session_state.min_rating]

if len(filtered) > 0:
    st.bar_chart(filtered.set_index("album")["rating"])

    # extra credit ( mean and median of data) 
    mean = filtered["rating"].mean()
    median = filtered["rating"].median()

    if "prev_mean" not in st.session_state:
        st.session_state.prev_mean = mean
        st.session_state.prev_median = median

    col1, col2 = st.columns(2)
    col1.metric("Mean rating", round(mean, 1), delta = round(mean - st.session_state.prev_mean, 1))
    col2.metric("Median rating", median, delta = median - st.session_state.prev_median)

    st.session_state.prev_mean = mean
    st.session_state.prev_median = median
else:
    st.write("No albums meet that minimum rating criteria.")
