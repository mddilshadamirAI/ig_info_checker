import streamlit as st
import json
import zipfile
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IG Full Data Pro", page_icon="📈", layout="wide")

st.title("📈 Instagram Full Analytics (JSON Edition)")
st.write("Extracting every detail including relationships and connection timelines.")

uploaded_file = st.file_uploader("Upload your Instagram JSON ZIP", type="zip")

def process_ig_json(z):
    all_files = z.namelist()
    
    # 1. FIND AND LOAD FOLLOWING
    following_path = next((f for f in all_files if 'following.json' in f), None)
    with z.open(following_path) as f:
        f_data = json.load(f)['relationships_following']
    
    # 2. FIND AND LOAD FOLLOWERS
    follower_files = [f for f in all_files if 'followers_' in f]
    ers_data = []
    for f_path in follower_files:
        with z.open(f_path) as f:
            ers_data.extend(json.load(f))
            
    # 3. CONVERT TO CLEAN DATAFRAMES
    def to_df(raw_list):
        return pd.DataFrame([{
            'username': item['string_list_data'][0]['value'],
            'timestamp': datetime.fromtimestamp(item['string_list_data'][0]['timestamp'])
        } for item in raw_list])

    df_ing = to_df(f_data)
    df_ers = to_df(ers_data)
    
    return df_ing, df_ers

if uploaded_file:
    try:
        df_ing, df_ers = process_ig_json(zipfile.ZipFile(uploaded_file))
        
        # LOGIC SETS
        ing_set = set(df_ing['username'])
        ers_set = set(df_ers['username'])
        
        unfollowers = ing_set - ers_set
        fans = ers_set - ing_set
        mutuals = ing_set.intersection(ers_set)

        # UI METRICS
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Following", len(ing_set))
        m2.metric("Followers", len(ers_set))
        m3.metric("Unfollowers", len(unfollowers))
        m4.metric("Mutuals", len(mutuals))

        # --- SECTION: TIMELINE ---
        st.subheader("📊 Your Instagram Growth Timeline")
        df_ing['Date'] = df_ing['timestamp'].dt.to_period('M').astype(str)
        timeline = df_ing.groupby('Date').size().reset_index(name='Count')
        
        fig = px.area(timeline, x='Date', y='Count', title="When you followed your current connections",
                      color_discrete_sequence=['#e1306c'])
        st.plotly_chart(fig, use_container_width=True)

        # --- SECTION: DEEP LISTS ---
        tab1, tab2, tab3 = st.tabs(["🐍 Unfollowers", "🤝 Mutuals & Fans", "📅 Detailed History"])
        
        with tab1:
            st.warning(f"Total: {len(unfollowers)} people")
            st.write(list(unfollowers))
            
        with tab2:
            col_a, col_b = st.columns(2)
            with col_a:
                st.info(f"Mutual Friends ({len(mutuals)})")
                st.write(list(mutuals))
            with col_b:
                st.success(f"Fans ({len(fans)})")
                st.write(list(fans))
                
        with tab3:
            st.subheader("Full Connection Log")
            st.write("This shows every account you follow and exactly when you followed them.")
            st.dataframe(df_ing.sort_values('timestamp', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Ensure your ZIP contains 'following.json' and 'followers_1.json' in JSON format.")
