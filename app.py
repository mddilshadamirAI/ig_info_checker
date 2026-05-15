import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="IG Insights Pro", page_icon="📸", layout="wide")

st.title("📸 Instagram Universal Analyzer")
st.info("Upload any Instagram Data ZIP file. This version automatically finds your data.")

uploaded_file = st.file_uploader("Upload your Instagram ZIP", type="zip")

def find_ig_data(z):
    all_files = z.namelist()
    following_data = []
    followers_data = []

    for file_path in all_files:
        if file_path.endswith('.json'):
            # Check for Following
            if 'following' in file_path.lower() and 'suggested' not in file_path.lower():
                try:
                    content = json.load(z.open(file_path))
                    # Extract list regardless of key name
                    data_list = content.get('relationships_following', content)
                    if isinstance(data_list, dict): 
                        data_list = data_list.get(list(data_list.keys())[0], [])
                    following_data.extend(data_list)
                except: continue

            # Check for Followers
            if 'followers' in file_path.lower():
                try:
                    content = json.load(z.open(file_path))
                    data_list = content.get('relationships_followers', content)
                    if isinstance(data_list, dict):
                        data_list = data_list.get(list(data_list.keys())[0], [])
                    followers_data.extend(data_list)
                except: continue

    return following_data, followers_data

if uploaded_file:
    try:
        with zipfile.ZipFile(uploaded_file) as z:
            following_raw, followers_raw = find_ig_data(z)

        if not following_raw or not followers_raw:
            st.error("No follower/following data found. Ensure you requested your data in JSON format.")
            st.stop()

        # Clean Data
        def clean(data):
            return pd.DataFrame([{
                'username': item['string_list_data'][0]['value'],
                'timestamp': datetime.fromtimestamp(item['string_list_data'][0]['timestamp'])
            } for item in data if 'string_list_data' in item])

        df_ing = clean(following_raw)
        df_ers = clean(followers_raw)

        # Logic
        ing_set = set(df_ing['username'])
        ers_set = set(df_ers['username'])
        
        unfollowers = ing_set - ers_set
        fans = ers_set - ing_set

        # UI
        c1, c2, c3 = st.columns(3)
        c1.metric("Following", len(ing_set))
        c2.metric("Followers", len(ers_set))
        c3.metric("Unfollowers", len(unfollowers))

        t1, t2 = st.tabs(["📊 Timeline", "🐍 Lists"])
        
        with t1:
            df_ing['Date'] = df_ing['timestamp'].dt.date
            fig = px.area(df_ing.groupby('Date').size().reset_index(name='Count'), 
                          x='Date', y='Count', title="Follow Activity")
            st.plotly_chart(fig, use_container_width=True)

        with t2:
            col_a, col_b = st.columns(2)
            col_a.subheader("Doesn't Follow Back")
            col_a.write(list(unfollowers))
            col_b.subheader("Your Fans")
            col_b.write(list(fans))

    except Exception as e:
        st.error(f"Processing Error: {e}")
