import streamlit as st
import pandas as pd
import zipfile
from bs4 import BeautifulSoup

st.set_page_config(page_title="IG Deep Intelligence", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ Instagram Deep Intelligence Tool")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your Instagram ZIP (HTML or JSON)", type="zip")

def get_users_from_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    users = []
    # IG HTML uses <a> tags for usernames and sometimes <td>
    for tag in soup.find_all(['a', 'td']):
        name = tag.get_text().strip()
        # Clean up common non-username strings found in IG HTML
        if name and "instagram.com" not in name.lower() and len(name) < 30 and " " not in name:
            users.append(name)
    return users

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as z:
        all_files = z.namelist()
        
        # Data Buckets
        following = []
        followers = []
        pending = []
        recent_activity = []

        for f_path in all_files:
            content = z.read(f_path)
            
            # 1. Extraction Logic
            if 'following' in f_path.lower() and f_path.endswith('.html'):
                following.extend(get_users_from_html(content))
            elif 'followers' in f_path.lower() and f_path.endswith('.html'):
                followers.extend(get_users_from_html(content))
            elif 'pending' in f_path.lower() and f_path.endswith('.html'):
                pending.extend(get_users_from_html(content))
            elif 'recent' in f_path.lower() and f_path.endswith('.html'):
                recent_activity.extend(get_users_from_html(content))

        # Cleanup & Sets
        following = sorted(list(set(following)))
        followers = sorted(list(set(followers)))
        pending = sorted(list(set(pending)))
        
        unfollowers = set(following) - set(followers)
        fans = set(followers) - set(following)
        mutuals = set(following).intersection(set(followers))

        # --- UI LAYOUT ---
        
        # Row 1: High Level Stats
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Following", len(following))
        c2.metric("Followers", len(followers))
        c3.metric("Mutuals", len(mutuals))
        c4.metric("Pending", len(pending))

        st.markdown("---")

        # Row 2: Tabs for Detail
        tab1, tab2, tab3, tab4 = st.tabs([
            "🐍 Unfollowers", 
            "⭐ Fans", 
            "🤝 Mutual Friends",
            "⏳ Pending Requests"
        ])

        with tab1:
            st.error(f"These {len(unfollowers)} people do not follow you back.")
            st.write(list(unfollowers))
        
        with tab2:
            st.success(f"These {len(fans)} people follow you (you don't follow back).")
            st.write(list(fans))
            
        with tab3:
            st.info("Your mutual connections.")
            st.write(list(mutuals))
            
        with tab4:
            if pending:
                st.warning("You sent follow requests to these users, but they haven't accepted.")
                st.write(pending)
            else:
                st.write("No pending requests found.")

        # Bonus: Download Results
        st.markdown("---")
        if unfollowers:
            csv = pd.DataFrame(list(unfollowers), columns=["Username"]).to_csv(index=False)
            st.download_button("📥 Download Unfollowers List", csv, "unfollowers.csv", "text/csv")

else:
    st.info("Waiting for ZIP upload. Please ensure you uploaded the full file from Instagram.")
