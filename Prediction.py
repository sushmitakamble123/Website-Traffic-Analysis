import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("🤖 Traffic Prediction")

data = pd.read_csv("data/traffic.csv")

X = data[['Users']]
y = data['PageViews']

model = LinearRegression()
model.fit(X, y)

user_input = st.number_input("Enter Expected Users", value=200)

prediction = model.predict([[user_input]])

st.success(f"Predicted Page Views: {int(prediction[0])}")
