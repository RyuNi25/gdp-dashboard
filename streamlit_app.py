import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = pd.read_csv("day.csv")  
    return df

df = load_data()

st.set_page_config(
    page_title="Bike Usage Analysis Dashboard",
    layout="wide"
)

st.title("🚴 Bike Usage Analysis Dashboard")
st.write("An interactive dashboard to explore bike usage trends and insights based on business questions.")

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", df['yr'].unique(), index=0)
selected_season = st.sidebar.selectbox("Select Season", ['All'] + list(df['season'].unique()), index=0)

filtered_df = df[df['yr'] == selected_year]
if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season'] == selected_season]

col1, col2 = st.columns(2)

with col1:
    yearly_usage = df.groupby('yr')['cnt'].sum().reset_index()
    plt.figure(figsize=(8, 4))
    sns.barplot(x=yearly_usage['yr'], y=yearly_usage['cnt'], palette="viridis")
    plt.title("Yearly Total Bike Usage", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Total Usage", fontsize=12)
    st.pyplot(plt.gcf())
    st.write("### Insight:")
    st.write("The total bike usage shows a year-over-year growth, indicating an increasing trend in bike adoption.")

with col2:
    user_types = filtered_df.groupby('workingday')[['casual', 'registered']].sum().reset_index()
    user_types = user_types.melt(id_vars='workingday', var_name='User Type', value_name='Count')
    plt.figure(figsize=(8, 4))
    sns.barplot(x='workingday', y='Count', hue='User Type', data=user_types, palette="viridis")
    plt.title("User Type Dominance on Working and Non-Working Days", fontsize=14)
    plt.xlabel("Working Day (1 = Yes, 0 = No)", fontsize=12)
    plt.ylabel("Total Users", fontsize=12)
    st.pyplot(plt.gcf())
    st.write("### Insight:")
    st.write("Registered users dominate on working days, while casual users are more prevalent on holidays.")

seasonal_usage = df.groupby('season')['cnt'].sum().reset_index()
st.subheader("Seasonal Impact on Bike Usage")
plt.figure(figsize=(10, 4))
sns.barplot(x='season', y='cnt', data=seasonal_usage, palette="viridis")
plt.title("Seasonal Impact on Bike Usage", fontsize=14)
plt.xlabel("Season", fontsize=12)
plt.ylabel("Total Usage", fontsize=12)
st.pyplot(plt.gcf())
st.write("### Insight:")
st.write("Spring and summer see the highest bike usage, suggesting that weather significantly influences user activity.")

monthly_usage = df.groupby('mnth')[['casual', 'registered']].sum().reset_index()
monthly_usage = monthly_usage.melt(id_vars='mnth', var_name='User Type', value_name='Count')
st.subheader("Monthly Usage: Casual vs Registered")
plt.figure(figsize=(10, 4))
sns.lineplot(x='mnth', y='Count', hue='User Type', data=monthly_usage, marker='o', palette="viridis")
plt.title("Monthly Usage by User Type", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Users", fontsize=12)
st.pyplot(plt.gcf())
st.write("### Insight:")
st.write("Bike usage peaks during mid-year months, aligning with warmer weather and vacation periods.")

rfm_summary = {
    'Recency': ["High (Recently Active)", "Medium", "Low (Inactive)"],
    'Frequency': ["High (Frequent Users)", "Medium", "Low"],
    'Monetary': ["High Contribution", "Medium", "Low"]
}
st.subheader("RFM Analysis Summary")
st.write(pd.DataFrame(rfm_summary))
st.write("### Insight:")
st.write("The RFM analysis identifies users' behavioral patterns, helping target marketing efforts effectively.")

st.write("---")
st.write("### Thank you for exploring the Bike Usage Analysis Dashboard! Feel free to reach out for any additional insights.")
