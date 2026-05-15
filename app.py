import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IG Full Analytics", page_icon="📈", layout="wide")

st.title("📈 Instagram Full Analytics (Error-Free Version)")
st.info("Built to handle both simple and nested JSON structures.")

uploaded_file = st.file_uploader("Upload Instagram JSON ZIP", type="zip")

def safe_extract(data):
    """Safely extracts usernames and timestamps regardless of JSON structure."""
    results = []
    # If data is a dictionary with a key like 'relationships_following'
    if isinstance(data, dict):
        key = next((k for k in data.keys() if 'following' in k or 'followers' in k), None)
        items = data.get(key, []) if key else []
    # If data is already a list (common in followers_1.json)
    elif isinstance(data, list):
        items = data
    else:
        items = []

    for entry in items:
        try:
            # Most common IG structure
            if 'string_list_data' in entry:
                info = entry['string_list_data'][0]
                results.append({
                    'username': info['value'],
                    'timestamp': datetime.fromtimestamp(info['timestamp'])
                })
            # Secondary backup for older/newer variations
            elif 'value' in entry:
                results.append({
                    'username': entry['value'],
                    'timestamp': datetime.fromtimestamp(entry.get('timestamp', 0))
                })
        except (KeyError, IndexError, TypeError):
            continue
    return pd.DataFrame(results)

if uploaded_file:
    try:
        with zipfile.ZipFile(uploaded_file) as z:
            all_files = z.namelist()
            
            # Load Following
            following_path = next((f for f in all_files if 'following.json' in f), None)
            df_ing = safe_extract(json.load(z.open(following_path))) if following_path else pd.DataFrame()
            
            # Load Followers (handles multiple files)
            follower_paths = [f for f in all_files if 'followers_' in f]
            ers_list = []
            for f_p in follower_paths:
                df_temp = safe_extract(json.load(z.open(f_p)))
                ers_list.append(df_temp)
            df_ers = pd.concat(ers_list) if ers_list else pd.DataFrame()

        if df_ing.empty or df_ers.empty:
            st.error("Could not find data. Ensure you selected 'JSON' and 'All Time' when downloading.")
        else:
            # Logic
            ing_set = set(df_ing['username'])
            ers_set = set(df_ers['username'])
            unfollowers = sorted(list(ing_set - ers_set))
            fans = sorted(list(ers_set - ing_set))
            mutuals = sorted(list(ing_set.intersection(ers_set)))

            # UI Metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Following", len(ing_set))
            c2.metric("Followers", len(ers_set))
            c3.metric("Unfollowers", len(unfollowers))
            c4.metric("Mutuals", len(mutuals))

            # Timeline Visual
            st.subheader("📊 Your Account History")
            df_ing['Month'] = df_ing['timestamp'].dt.to_period('M').astype(str)
            timeline = df_ing.groupby('Month').size().reset_index(name='Follows')
            fig = px.bar(timeline, x='Month', y='Follows', title="Monthly Follow Activity", color_discrete_sequence=['#833ab4'])
            st.plotly_chart(fig, use_container_width=True)

            # Detail Tabs
            t1, t2, t3 = st.tabs(["🐍 Unfollowers", "🤝 Mutuals & Fans", "📅 Full History"])
            with t1: st.write(unfollowers)
            with t2:
                col_a, col_b = st.columns(2)
                col_a.write("**Mutuals:**"); col_a.write(mutuals)
                col_b.write("**Fans:**"); col_b.write(fans)
            with t3: st.dataframe(df_ing.sort_values('timestamp', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")

else:
    st.info("Upload your JSON ZIP. Ensure it is the 'Followers and Following' file.")
