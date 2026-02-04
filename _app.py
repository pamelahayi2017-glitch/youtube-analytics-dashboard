import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Page config
# =========================
st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

# =========================
# Title
# =========================
st.title("📊 YouTube Analytics Dashboard")
st.markdown("Interactive dashboard for YouTube performance, engagement, and trend analysis")

# =========================
# Load data
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("youtube_data.csv")

df = load_data()

# =========================
# Feature engineering
# =========================
df['Engagement'] = df['Likes'] + df['Comments']
df['Engagement_Rate'] = (df['Engagement'] / df['Views']) * 100
df['Upload_Date'] = pd.to_datetime(df['Upload_Date'])

# =========================
# Sidebar filters
# =========================
st.sidebar.header("🎛 Filters")

channel_filter = st.sidebar.multiselect(
    "Select Channel",
    options=df['Channel'].unique(),
    default=df['Channel'].unique()
)

df_filtered = df[df['Channel'].isin(channel_filter)]

# =========================
# KPI Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Videos", df_filtered.shape[0])
col2.metric("Total Views", int(df_filtered['Views'].sum()))
col3.metric("Total Likes", int(df_filtered['Likes'].sum()))
col4.metric("Avg Engagement Rate (%)", round(df_filtered['Engagement_Rate'].mean(), 2))

st.markdown("---")

# =========================
# Charts Layout
# =========================
left, right = st.columns(2)

# Views by Channel
with left:
    st.subheader("Views by Channel")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=df_filtered, x='Channel', y='Views', ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# Engagement Rate by Channel
with right:
    st.subheader("Engagement Rate by Channel")
    fig2, ax2 = plt.subplots()
    sns.barplot(data=df_filtered, x='Channel', y='Engagement_Rate', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.markdown("---")

# =========================
# Trend Analysis
# =========================
st.subheader("📈 Views Trend Over Time")

trend_df = df_filtered.sort_values("Upload_Date")

fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(data=trend_df, x='Upload_Date', y='Views', ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.markdown("---")

# =========================
# Top Videos Table
# =========================
st.subheader("🔥 Top Performing Videos")

top_videos = df_filtered.sort_values(by="Views", ascending=False).head(10)
st.dataframe(top_videos[['Title', 'Channel', 'Views', 'Likes', 'Comments', 'Engagement_Rate']])

st.markdown("---")

# =========================
# Footer
# =========================
st.markdown("**Project:** YouTube Data Analytics & Prediction Dashboard")
st.markdown("**Built with:** Python, Pandas, Seaborn, Matplotlib, Streamlit")
st.markdown("**Author:** Portfolio Project")
