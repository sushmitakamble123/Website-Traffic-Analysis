import streamlit as st
import pandas as pd

st.title("📊 Data Analysis")

data = pd.read_csv("data/traffic.csv")

st.write("Dataset Preview")
st.dataframe(data)

st.write("Summary")
st.write(data.describe())
