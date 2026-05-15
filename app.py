import streamlit as st
import pandas as pd
import zipfile
import json
from bs4 import BeautifulSoup
import plotly.express as px

st.set_page_config(page_title="Universal IG Analyzer", page_icon="📸")

st.title("📸 Universal Instagram Analyzer")
st.info("Upload your ZIP. Supports both HTML and JSON formats.")

uploaded_file = st.file_uploader("Upload Instagram ZIP", type="zip")

def extract_usernames(file_content, is_json=True):
    usernames = []
    if is_json:
        try:
            data = json.loads(file_content)
            # Find the list of users in nested JSON
            raw_list = data.get('relationships_following', data)
            if isinstance(raw_list, dict):
                raw_list = raw_list.get(list(raw_list.keys())[0], [])
            for item in raw_list:
                if 'string_list_data' in item:
                    usernames.append(item['string_list_data'][0]['value'])
        except: pass
    else:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(file_content, 'lxml')
        # Instagram HTML puts usernames in <a> tags
        for a in soup.find_all('a'):
            name = a.get_text().strip()
            if name and "instagram.com" not in name.lower():
                usernames.append(name)
    return usernames

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as z:
        all_files = z.namelist()
        following = []
        followers = []

        for f_path in all_files:
            # Check for Following files
            if 'following' in f_path.lower():
                is_json = f_path.endswith('.json')
                following.extend(extract_usernames(z.read(f_path), is_json))
            
            # Check for Followers files
            if 'followers' in f_path.lower():
                is_json = f_path.endswith('.json')
                followers.extend(extract_usernames(z.read(f_path), is_json))

        # Cleanup
        following = sorted(list(set(following)))
        followers = sorted(list(set(followers)))

        if not following or not followers:
            st.error("No data found. Ensure you selected 'Followers and Following' during download.")
        else:
            unfollowers = set(following) - set(followers)
            fans = set(followers) - set(following)

            # UI Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Following", len(following))
            c2.metric("Followers", len(followers))
            c3.metric("Unfollowers", len(unfollowers), delta_color="inverse")

            tab1, tab2 = st.tabs(["🐍 Unfollowers", "⭐ Fans"])
            with tab1:
                st.subheader("People who don't follow you back")
                st.write(list(unfollowers))
            with tab2:
                st.subheader("Your Fans (They follow, you don't)")
                st.write(list(fans))
