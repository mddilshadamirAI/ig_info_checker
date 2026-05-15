import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IG Full Analytics 2026", page_icon="📈", layout="wide")

st.title("📈 Instagram Full Analytics & Timeline")
st.info("Upload your JSON ZIP to see unfollowers, mutuals, and your growth history.")

uploaded_file = st.file_uploader("Upload Instagram JSON ZIP", type="zip")

def extract_data(z):
    all_files = z.namelist()
    
    # 1. LOAD FOLLOWING (Usually has a wrapper key)
    following_path = next((f for f in all_files if 'following.json' in f), None)
    with z.open(following_path) as f:
        f_raw = json.load(f)
        # Handle cases where it's wrapped in 'relationships_following'
        f_list = f_raw.get('relationships_following', f_raw)
    
    # 2. LOAD FOLLOWERS (Usually a direct list)
    follower_files = [f for f in all_files if 'followers_' in f]
    ers_list = []
    for f_path in follower_files:
        with z.open(f_path) as f:
            ers_list.extend(json.load(f))
            
    # 3. HELPER TO CONVERT TO DATAFRAME
    def to_df(data_list):
        rows = []
        for item in data_list:
            try:
                # Instagram's structure: [{'string_list_data': [{'value': 'name', 'timestamp': 123}]}]
                info = item['string_list_data'][0]
                rows.append({
                    'username': info['value'],
                    'timestamp': datetime.fromtimestamp(info['timestamp'])
                })
            except (KeyError, IndexError):
                continue
        return pd.DataFrame(rows)

    return to_df(f_list), to_df(ers_list)

if uploaded_file:
    try:
        with zipfile.ZipFile(uploaded_file) as z:
            df_ing, df_ers = extract_data(z)
        
        # LOGIC
        ing_set = set(df_ing['username'])
        ers_set = set(df_ers['username'])
        
        unfollowers = sorted(list(ing_set - ers_set))
        fans = sorted(list(ers_set - ing_set))
        mutuals = sorted(list(ing_set.intersection(ers_set)))

        # UI METRICS
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Following", len(ing_set))
        c2.metric("Followers", len(ers_set))
        c3.metric("Unfollowers", len(unfollowers), delta_color="inverse")
        c4.metric("Mutuals", len(mutuals))

        # --- VISUALIZATION: TIMELINE ---
        st.subheader("📊 Connection History (Growth Timeline)")
        # We use the Following data to show when you discovered new people
        df_ing['Month-Year'] = df_ing['timestamp'].dt.to_period('M').astype(str)
        timeline = df_ing.groupby('Month-Year').size().reset_index(name='New Connections')
        
        fig = px.line(timeline, x='Month-Year', y='New Connections', 
                      title="Follow Activity Over Time",
                      line_shape='spline', markers=True)
        fig.update_traces(line_color='#e1306c')
        st.plotly_chart(fig, use_container_width=True)

        # --- DEEP DATA TABS ---
        t1, t2, t3, t4 = st.tabs(["🐍 Unfollowers", "⭐ Fans", "🤝 Mutuals", "📋 Full Log"])
        
        with t1:
            st.error(f"These {len(unfollowers)} people do not follow you back.")
            st.write(unfollowers)
        with t2:
            st.success(f"These {len(fans)} people follow you, but you don't follow them.")
            st.write(fans)
        with t3:
            st.info("Accounts where you both follow each other.")
            st.write(mutuals)
        with t4:
            st.subheader("Raw History Data")
            st.dataframe(df_ing.sort_values('timestamp', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Double-check that you downloaded your data in **JSON** format, not HTML.")

else:
    st.info("Waiting for JSON ZIP upload...")
