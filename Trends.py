import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Traffic Trends")

data = pd.read_csv("data/traffic.csv")

fig = px.line(data, x='Date', y='Users', title="User Growth")
st.plotly_chart(fig)

fig2 = px.bar(data, x='Source', y='PageViews', title="Traffic by Source")
st.plotly_chart(fig2)
