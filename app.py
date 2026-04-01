import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from database import add_user, login_user

st.set_page_config(page_title="Traffic Dashboard", layout="wide")

# ---------------- SESSION ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    data = pd.read_csv("traffic.csv")

    # Fix date format
    data['Date'] = pd.to_datetime(data['Date'], format='mixed', errors='coerce')
    data = data.dropna(subset=['Date'])

    return data

# ---------------- SIGNUP ---------------- #
def signup():
    st.title("📝 Signup")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Create Account"):
        add_user(new_user, new_pass)
        st.success("Account created successfully ✅")

# ---------------- LOGIN ---------------- #
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login_user(username, password)
        if result:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

# ---------------- DASHBOARD ---------------- #
def dashboard():
    st.title("🌐 Website Traffic Dashboard")

    data = load_data()

    # Sidebar
    st.sidebar.success(f"Welcome {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ---------------- FILTER ---------------- #
    source = st.sidebar.selectbox("Select Source", data['Source'].unique())
    filtered_data = data[data['Source'] == source]

    # ---------------- METRICS ---------------- #
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", int(filtered_data['Users'].sum()))
    col2.metric("Total Page Views", int(filtered_data['PageViews'].sum()))
    col3.metric("Avg Bounce Rate", round(filtered_data['BounceRate'].mean(), 2))

    # ---------------- GRAPHS ---------------- #
    fig1 = px.line(filtered_data, x='Date', y='Users', title="User Growth")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(filtered_data, x='Date', y='PageViews', title="Page Views")
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- TODAY VS YESTERDAY ---------------- #
    st.subheader("📊 Today vs Yesterday Status")

    data = data.sort_values("Date")

    if len(data) >= 2:
        today = data.iloc[-1]
        yesterday = data.iloc[-2]

        change = today['Users'] - yesterday['Users']

        st.write(f"📅 Today: {today['Date'].date()}")
        st.write(f"📅 Yesterday: {yesterday['Date'].date()}")

        col1, col2 = st.columns(2)
        col1.metric("Today Users", int(today['Users']))
        col2.metric("Yesterday Users", int(yesterday['Users']))

        st.metric("User Change", int(change))

        if change > 0:
            st.success("📈 Traffic Increased")
        elif change < 0:
            st.error("📉 Traffic Decreased")
        else:
            st.warning("⚖ No Change")
    else:
        st.warning("Not enough data")

    # ---------------- LAST 30 DAYS ---------------- #
    st.subheader("📅 Last 30 Days Analysis")

    last_month = data[data['Date'] >= (pd.Timestamp.today() - pd.Timedelta(days=30))]

    st.write("Total Users:", int(last_month['Users'].sum()))
    st.write("Total PageViews:", int(last_month['PageViews'].sum()))

    fig3 = px.line(last_month, x='Date', y='Users', title="Last 30 Days Trend")
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------- PREDICTION ---------------- #
    st.subheader("🤖 Prediction")

    data['Day'] = data['Date'].dt.day
    data['Month'] = data['Date'].dt.month

    X = data[['Users', 'Day', 'Month']]
    y = data['PageViews']

    model = RandomForestRegressor()
    model.fit(X, y)

    user_input = st.number_input("Enter Expected Users", value=200)

    import datetime
    today_date = datetime.datetime.today()

    input_data = [[user_input, today_date.day, today_date.month]]

    prediction = model.predict(input_data)

    st.success(f"🔮 Predicted Page Views: {int(prediction[0])}")

# ---------------- MENU ---------------- #
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if st.session_state.logged_in:
    dashboard()
else:
    if choice == "Login":
        login()
    else:
        signup()
