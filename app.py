import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CellWatch", layout="wide")
st.title("CellWatch: Cellular Network Outage Tracker")
st.caption("Note: data is simulated for demonstration.")

df = pd.read_csv("outages.csv")
df["date"] = pd.to_datetime(df["date"])

# Sidebar filters
st.sidebar.header("Filters")
operators = st.sidebar.multiselect(
    "Operator", sorted(df["operator"].unique()), default=sorted(df["operator"].unique())
)
cities = st.sidebar.multiselect(
    "City", sorted(df["city"].unique()), default=sorted(df["city"].unique())
)
filtered = df[df["operator"].isin(operators) & df["city"].isin(cities)]

# Summary numbers
c1, c2, c3 = st.columns(3)
c1.metric("Total outages", len(filtered))
c2.metric("Average duration (min)", round(filtered["duration_minutes"].mean(), 1))
c3.metric("Longest outage (min)", filtered["duration_minutes"].max())

# Charts
left, right = st.columns(2)
by_op = filtered.groupby("operator").size().reset_index(name="outages")
left.plotly_chart(px.bar(by_op, x="operator", y="outages", title="Outages per operator"),
                  use_container_width=True)
right.plotly_chart(px.pie(filtered, names="cause", title="Causes of outages"),
                   use_container_width=True)

by_city = filtered.groupby("city")["duration_minutes"].mean().reset_index()
st.plotly_chart(px.bar(by_city, x="city", y="duration_minutes",
                       title="Average outage duration by city (minutes)"),
                use_container_width=True)

# Raw data
st.subheader("Data table")
st.dataframe(filtered, use_container_width=True)