import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IG Analytics Pro", layout="wide")

st.title("📸 The Ultimate IG JSON Analyzer")
st.write("This version is designed to bypass all 'String Index' and 'Key' errors.")

uploaded_file = st.file_uploader("Upload your JSON ZIP", type="zip")

def get_deep_data(data):
    """Recursively finds all username/timestamp pairs in any JSON structure."""
    extracted = []
    
    if isinstance(data, list):
        for item in data:
            extracted.extend(get_deep_data(item))
    elif isinstance(data, dict):
        # Check if this specific dictionary has the user data we want
        if 'string_list_data' in data and isinstance(data['string_list_data'], list):
            info = data['string_list_data'][0]
            extracted.append({
                'username': info.get('value', 'Unknown'),
                'timestamp': datetime.fromtimestamp(info.get('timestamp', 0))
            })
        else:
            # Otherwise, keep digging into all keys
            for key, value in data.items():
                extracted.extend(get_deep_data(value))
    return extracted

if uploaded_file:
    try:
        with zipfile.ZipFile(uploaded_file) as z:
            all_files = z.namelist()
            
            # Find following.json
            f_path = next((f for f in all_files if 'following.json' in f), None)
            following_raw = json.load(z.open(f_path)) if f_path else {}
            df_ing = pd.DataFrame(get_deep_data(following_raw)).drop_duplicates('username')
            
            # Find all followers_x.json files
            er_paths = [f for f in all_files if 'followers_' in f and f.endswith('.json')]
            all_ers = []
            for p in er_paths:
                all_ers.extend(get_deep_data(json.load(z.open(p))))
            df_ers = pd.DataFrame(all_ers).drop_duplicates('username')

        if df_ing.empty or df_ers.empty:
            st.error("Wait! The script ran but found 0 users. Check if your ZIP has JSON files inside.")
        else:
            # Analytics Logic
            ing_set = set(df_ing['username'])
            ers_set = set(df_ers['username'])
            
            unfollowers = sorted(list(ing_set - ers_set))
            fans = sorted(list(ers_set - ing_set))
            mutuals = sorted(list(ing_set.intersection(ers_set)))

            # --- DISPLAY ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Following", len(ing_set))
            c2.metric("Followers", len(ers_set))
            c3.metric("Unfollowers", len(unfollowers))
            c4.metric("Mutuals", len(mutuals))

            st.subheader("📊 Your Account History")
            df_ing['Month'] = df_ing['timestamp'].dt.to_period('M').astype(str)
            timeline = df_ing.groupby('Month').size().reset_index(name='New Follows')
            st.plotly_chart(px.area(timeline, x='Month', y='New Follows', color_discrete_sequence=['#833ab4']), use_container_width=True)

            t1, t2 = st.tabs(["🐍 Unfollowers", "📅 Full Connection History"])
            with t1:
                st.write(unfollowers)
            with t2:
                st.dataframe(df_ing.sort_values('timestamp', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Critical Error: {e}")
