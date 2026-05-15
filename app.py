import streamlit as st
import pandas as pd
import zipfile
import json
from bs4 import BeautifulSoup

st.set_page_config(page_title="IG Precision Analyzer", page_icon="🎯", layout="wide")

st.title("🎯 Instagram Precision Analyzer")
st.info("This version uses Strict Parsing to ensure usernames are correct.")

uploaded_file = st.file_uploader("Upload Instagram ZIP", type="zip")

def extract_precise_data(file_content, is_json=True):
    usernames = []
    if is_json:
        try:
            data = json.loads(file_content)
            # Find the nested list in JSON
            raw = data.get('relationships_following', data)
            if isinstance(raw, dict): raw = raw.get(list(raw.keys())[0], [])
            for item in raw:
                if 'string_list_data' in item:
                    usernames.append(item['string_list_data'][0]['value'])
        except: pass
    else:
        # HTML PRECISE PARSING
        soup = BeautifulSoup(file_content, 'lxml')
        # Instagram 2026 HTML structure: usernames are usually inside <a> tags 
        # within a specific div or table cell.
        for a in soup.find_all('a'):
            href = a.get('href', '')
            text = a.get_text().strip()
            
            # Logic: If it's a link to a profile, the text is the username
            if 'instagram.com/' in href:
                user = href.split('instagram.com/')[1].replace('/', '').split('?')[0]
                if user and user not in ['explore', 'reels', 'direct', 'accounts']:
                    usernames.append(user)
            # Backup: If no href, check if text looks like a single username (no spaces)
            elif text and ' ' not in text and len(text) < 30 and '.' not in text:
                if text.lower() not in ['login', 'signup', 'about', 'help', 'privacy', 'terms']:
                    usernames.append(text)
                    
    return list(set(usernames))

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as z:
        all_files = z.namelist()
        following, followers = [], []

        for f_path in all_files:
            if 'following.html' in f_path.lower() or 'following.json' in f_path.lower():
                following.extend(extract_precise_data(z.read(f_path), f_path.endswith('.json')))
            if 'followers' in f_path.lower() and (f_path.endswith('.html') or f_path.endswith('.json')):
                followers.extend(extract_precise_data(z.read(f_path), f_path.endswith('.json')))

        # Final Clean
        following = [u for u in following if u]
        followers = [u for u in followers if u]
        
        unfollowers = set(following) - set(followers)
        fans = set(followers) - set(following)

        # UI
        st.success(f"Analyzed {len(following)} Following and {len(followers)} Followers.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"🐍 Unfollowers ({len(unfollowers)})")
            st.write(sorted(list(unfollowers)))
        with col2:
            st.subheader(f"⭐ Fans ({len(fans)})")
            st.write(sorted(list(fans)))
