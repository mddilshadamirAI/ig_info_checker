import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="IG Insights Pro", page_icon="📸", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Instagram Relationship & Timeline Analyzer")
st.info("Upload your 'connections' ZIP file from Instagram to see deep insights.")

# File Uploader
uploaded_file = st.file_uploader("Upload your connections.zip", type="zip")

def get_data_from_zip(zip_file):
    with zipfile.ZipFile(zip_file) as z:
        all_files = z.namelist()
        
        # SMART SEARCH: Find the files regardless of folder structure
        following_path = next((f for f in all_files if 'following.json' in f), None)
        follower_paths = [f for f in all_files if 'followers_' in f and f.endswith('.json')]
        
        if not following_path:
            st.error("❌ Could not find 'following.json'. Ensure you selected 'JSON' format in Instagram Settings.")
            st.stop()
        if not follower_paths:
            st.error("❌ Could not find any 'followers_x.json' files.")
            st.stop()

        # Load following
        following_raw = json.load(z.open(following_path))
        # Handle different IG JSON versions (sometimes it's under 'relationships_following', sometimes others)
        if isinstance(following_raw, dict) and 'relationships_following' in following_raw:
            following_list = following_raw['relationships_following']
        elif isinstance(following_raw, list):
            following_list = following_raw
        else:
            # Fallback for newer 2026 formats
            first_key = list(following_raw.keys())[0]
            following_list = following_raw[first_key]
        
        # Load followers (handles multiple files like followers_1.json, followers_2.json)
        followers_list = []
        for f in follower_paths:
            data = json.load(z.open(f))
            # Some formats wrap followers in a list directly, others use a dict
            if isinstance(data, list):
                followers_list.extend(data)
            else:
                first_key = list(data.keys())[0]
                followers_list.extend(data[first_key])
            
        return following_list, followers_list

if uploaded_file:
    try:
        following_data, followers_data = get_data_from_zip(uploaded_file)

        # 1. Processing Data into DataFrames
        following_df = pd.DataFrame([{
            'username': item['string_list_data'][0]['value'],
            'timestamp': datetime.fromtimestamp(item['string_list_data'][0]['timestamp'])
        } for item in following_data])

        followers_df = pd.DataFrame([{
            'username': item['string_list_data'][0]['value'],
            'timestamp': datetime.fromtimestamp(item['string_list_data'][0]['timestamp'])
        } for item in followers_data])

        # 2. Logic Sets
        following_set = set(following_df['username'])
        followers_set = set(followers_df['username'])

        not_following_back = following_set - followers_set
        fans = followers_set - following_set
        mutuals = following_set.intersection(followers_set)

        # 3. UI Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Following", len(following_set))
        col2.metric("Followers", len(followers_set))
        col3.metric("Not Following Back", len(not_following_back), delta_color="inverse")
        col4.metric("Fans", len(fans))

        # 4. Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Timeline & Trends", "🐍 Unfollowers", "⭐ Fans & Mutuals"])

        with tab1:
            st.subheader("Your Instagram Growth Timeline")
            following_df['Month-Year'] = following_df['timestamp'].dt.to_period('M').astype(str)
            timeline_data = following_df.groupby('Month-Year').size().reset_index(name='Count')
            
            fig = px.line(timeline_data, x='Month-Year', y='Count', title='Account Connection Activity Over Time',
                          labels={'Count': 'New Follows', 'Month-Year': 'Date'},
                          line_shape='spline')
            fig.update_traces(line_color='#e1306c', line_width=4)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("People who don't follow you back")
            if not_following_back:
                df_unfollowers = following_df[following_df['username'].isin(not_following_back)].sort_values('timestamp', ascending=False)
                st.dataframe(df_unfollowers[['username', 'timestamp']], use_container_width=True)
            else:
                st.success("Everyone follows you back! 🎉")

        with tab3:
            col_fans, col_mut = st.columns(2)
            with col_fans:
                st.subheader("Your Fans (Followers you don't follow back)")
                st.write(list(fans))
            with col_mut:
                st.subheader("Mutual Friends")
                st.write(list(mutuals))

    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.warning("Note: Ensure you downloaded 'JSON' format, not HTML.")

else:
    st.info("Please upload the ZIP file you received from Instagram.")
