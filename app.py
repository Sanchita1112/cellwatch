import streamlit as st
import pandas as pd
import plotly.express as px

st.title("CellWatch: Cellular Network Outage Tracker")

df = pd.read_csv("outages.csv")

operator = st.selectbox("Choose operator", df["operator"].unique())
filtered = df[df["operator"] == operator]

st.write("Total outages:", len(filtered))
st.plotly_chart(px.bar(filtered, x="city", y="duration_minutes"))