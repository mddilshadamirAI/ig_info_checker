import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IG Deep Insight", page_icon="🔍", layout="wide")

st.title("🔍 Instagram Deep Data Scanner")
st.info("Upload your ZIP. This version searches every hidden folder in your file.")

uploaded_file = st.file_uploader("Upload Instagram ZIP", type="zip")

def deep_scan_zip(z):
    following_list = []
    followers_list = []
    
    for file_path in z.namelist():
        if file_path.endswith('.json'):
            try:
                with z.open(file_path) as f:
                    data = json.load(f)
                    
                    # Detect Following Data (looking for the structure, not the name)
                    if "relationships_following" in str(data) or "following" in file_path.lower():
                        # Extract the actual list from various possible keys
                        raw = data.get('relationships_following', data)
                        if isinstance(raw, dict): raw = raw.get(list(raw.keys())[0], [])
                        following_list.extend(raw)
                        
                    # Detect Followers Data
                    if "relationships_followers" in str(data) or "followers" in file_path.lower():
                        raw = data.get('relationships_followers', data)
                        if isinstance(raw, dict): raw = raw.get(list(raw.keys())[0], [])
                        followers_list.extend(raw)
            except:
                continue
    return following_list, followers_list

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as z:
        # Show the user what's inside their zip if it fails
        all_files = z.namelist()
        
        with st.expander("See Files Found in ZIP"):
            st.write(all_files)

        ing, ers = deep_scan_zip(z)

        if not ing or not ers:
            st.error("🚨 NO DATA FOUND INSIDE ZIP.")
            st.write("Current Files in ZIP:", all_files[:10], "...and more.")
            st.warning("IMPORTANT: When you requested the download, did you click 'JSON' or 'HTML'? This script only works with JSON.")
            st.stop()

        # Cleaner function for IG's weird nested structure
        def process(rows):
            results = []
            for item in rows:
                try:
                    # Logic to find the username and timestamp in various IG versions
                    user_data = item.get('string_list_data', [{}])[0]
                    results.append({
                        'username': user_data.get('value', 'Unknown'),
                        'timestamp': datetime.fromtimestamp(user_data.get('timestamp', 0))
                    })
                except: continue
            return pd.DataFrame(results)

        df_ing = process(ing).drop_duplicates('username')
        df_ers = process(ers).drop_duplicates('username')

        # Calculation
        not_back = set(df_ing['username']) - set(df_ers['username'])
        
        st.success(f"Successfully found {len(df_ing)} Following and {len(df_ers)} Followers!")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Total Unfollowers", len(not_back))
            st.subheader("🐍 They don't follow back:")
            st.write(list(not_back))
            
        with c2:
            st.subheader("📈 Follow History")
            df_ing['Date'] = df_ing['timestamp'].dt.date
            chart_data = df_ing.groupby('Date').size().reset_index(name='Count')
            st.line_chart(chart_data.set_index('Date'))

else:
    st.write("Please upload your file to begin.")
