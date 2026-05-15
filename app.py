import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IG Deep Recovery", layout="wide")

st.title("🛡️ Instagram Data Recovery & Timeline")
st.info("This version scans the RAW JSON code to find your lost data.")

uploaded_file = st.file_uploader("Upload JSON ZIP", type="zip")

def universal_parser(obj):
    """Deep-scans any JSON object for usernames and timestamps."""
    found = []
    if isinstance(obj, dict):
        # Look for the specific 'value' and 'timestamp' keys regardless of where they are
        if 'value' in obj and 'timestamp' in obj:
            found.append({
                'user': obj['value'],
                'time': datetime.fromtimestamp(obj['timestamp'])
            })
        else:
            for v in obj.values():
                found.extend(universal_parser(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(universal_parser(item))
    return found

if uploaded_file:
    try:
        with zipfile.ZipFile(uploaded_file) as z:
            # 1. SCAN EVERYTHING
            all_following = []
            all_followers = []
            
            for file_path in z.namelist():
                if file_path.endswith('.json'):
                    with z.open(file_path) as f:
                        data = json.load(f)
                        extracted = universal_parser(data)
                        
                        if 'following' in file_path.lower():
                            all_following.extend(extracted)
                        elif 'followers' in file_path.lower():
                            all_followers.extend(extracted)

        # 2. CREATE CLEAN TABLES
        df_ing = pd.DataFrame(all_following).drop_duplicates('user')
        df_ers = pd.DataFrame(all_followers).drop_duplicates('user')

        if df_ing.empty or df_ers.empty:
            st.error("Data was found but couldn't be parsed. Are you sure this is a JSON export?")
        else:
            # 3. ANALYSIS
            ing_set = set(df_ing['user'])
            ers_set = set(df_ers['user'])
            
            unfollowers = sorted(list(ing_set - ers_set))
            fans = sorted(list(ers_set - ing_set))
            mutuals = sorted(list(ing_set.intersection(ers_set)))

            # 4. DASHBOARD
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Following", len(ing_set))
            c2.metric("Followers", len(ers_set))
            c3.metric("Unfollowers", len(unfollowers))
            c4.metric("Mutuals", len(mutuals))

            # --- GROWTH CHART ---
            st.subheader("📊 Your Account History")
            df_ing['Month'] = df_ing['time'].dt.to_period('M').astype(str)
            chart_data = df_ing.groupby('Month').size().reset_index(name='Count')
            st.plotly_chart(px.line(chart_data, x='Month', y='Count', markers=True, 
                                    title="When you added people", 
                                    line_shape='spline'), use_container_width=True)

            # --- LISTS ---
            t1, t2, t3 = st.tabs(["🐍 Not Following Back", "🤝 Mutuals", "📋 History"])
            t1.write(unfollowers)
            t2.write(mutuals)
            t3.dataframe(df_ing.sort_values('time', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Founder, we hit a block: {e}")
