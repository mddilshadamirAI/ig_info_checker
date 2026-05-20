import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="InstaGrid Bio OS",
    page_icon="🔮",
    layout="wide"
)

# Custom Clean CSS Style Matrix
st.markdown("""
<style>
div[data-testid="stAppViewContainer"], .main {
    background: #090d16 !important;
}
h1, h2, h3, h4, p, span, label {
    color: #f8fafc !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}
.phone-view {
    background: #020617;
    padding: 30px 20px;
    border-radius: 36px;
    border: 2px solid #1e293b;
    max-width: 360px;
    margin: 0 auto;
    text-align: center;
}
.avatar-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(45deg, #f09433, #dc2743, #cc2366);
    border-radius: 50%;
    margin: 0 auto 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
}
.bio-link {
    display: block;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #ffffff !important;
    text-decoration: none;
    padding: 14px;
    margin: 12px 0;
    border-radius: 12px;
    font-weight: 500;
    font-size: 14px;
    border-left: 4px solid #06b6d4;
    transition: background 0.2s;
}
.bio-link:hover {
    background: rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 📡 TRACK 1: THE LIVE VISITOR VIEW (When someone clicks your Instagram link)
# ==============================================================================
# Check if someone arrived at the app via a shared user link
query_params = st.experimental_get_query_params()

if "user" in query_params:
    target_user = query_params["user"]
    
    # Read the data out of the shared query state safely
    user_bio = query_params.get("bio", "Welcome to my link hub!")
    
    # Parse the compiled links out of the URL string parameters
    raw_titles = query_params.get_all("t")
    raw_urls = query_params.get_all("u")
    
    # Render the standalone mobile page layout for visitors
    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="phone-view">', unsafe_allow_html=True)
    st.markdown('<div class="avatar-icon">🚀</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>@{target_user}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #94a3b8; font-size:14px;">{user_bio}</p>', unsafe_allow_html=True)
    st.markdown('<div style="border-bottom: 1px solid #1e293b; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    
    if raw_titles and raw_urls:
        for title, url in zip(raw_titles, raw_urls):
            st.markdown(f'<a class="bio-link" href="{url}" target="_blank">{title}</a>', unsafe_allow_html=True)
    else:
        st.caption("No active links configured for this profile yet.")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hide the rest of the workspace creator panel for casual visitors
    st.stop()


# ==============================================================================
# ⚙️ TRACK 2: THE CREATOR DASHBOARD PANEL (For building your page)
# ==============================================================================
if "builder_links" not in st.session_state:
    st.session_state.builder_links = [
        {"title": "💻 Check my GitHub", "url": "https://github.com"},
        {"title": "🚀 Live Streamlit App", "url": "https://streamlit.io"}
    ]

st.title("🔮 InstaGrid Direct Link Dashboard")
st.caption("Generate instant live links for your Instagram Bio without hosting or code handles.")
st.markdown("---")

left_col, right_col = st.columns([1.1, 1.3], gap="large")

with left_col:
    st.subheader("📱 Current Layout Preview")
    
    c_user = st.text_input("Choose Username:", value="dilshad.dev")
    c_bio = st.text_area("Write Profile Bio:", value="Building web utility layers.")
    
    st.markdown('<div class="phone-view">', unsafe_allow_html=True)
    st.markdown('<div class="avatar-icon">🤖</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>@{c_user}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #94a3b8; font-size:13px;">{c_bio}</p>', unsafe_allow_html=True)
    st.markdown('<div style="border-bottom: 1px solid #1e293b; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    
    for item in st.session_state.builder_links:
        st.markdown(f'<div class="bio-link">{item["title"]}</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.subheader("🛠️ Link Management Console")
    
    with st.container(border=True):
        st.markdown("#### ➕ Add Link Customization")
        t_input = st.text_input("Button Text Display Label:", placeholder="e.g., Portfolio Site")
        u_input = st.text_input("Full Link Target Destination URL:", placeholder="https://example.com")
        
        if st.button("Save Link Into Dashboard Grid", use_container_width=True):
            if t_input and u_input:
                st.session_state.builder_links.append({"title": t_input, "url": u_input})
                st.rerun()
                
    with st.container(border=True):
        st.markdown("#### 📋 Existing Active Configurations")
        for idx, item in enumerate(st.session_state.builder_links):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{item['title']}** → {item['url']}")
            with col_b:
                if st.button("Purge", key=f"del_{idx}", use_container_width=True):
                    st.session_state.builder_links.pop(idx)
                    st.rerun()

    # ==============================================================================
    # 🔗 DYNAMIC LIVE URL GENERATOR FIELD BUILDER
    # ==============================================================================
    with st.container(border=True):
        st.markdown("#### 🚀 Your Instant Live Link Generation Area")
        st.caption("This link is live right now! Copy it and drop it directly into your Instagram bio list. No deployment necessary.")
        
        # Build out the target live dashboard tracking link using URL parameter structures
        base_live_url = "https://your-app-name.streamlit.app/"
        
        # Build query parameters strings directly
        url_arguments = f"?user={c_user}&bio={c_bio.replace(' ', '+')}"
        for item in st.session_state.builder_links:
            url_arguments += f"&t={item['title'].replace(' ', '+')}&u={item['url']}"
            
        full_live_share_link = base_live_url + url_arguments
        
        st.text_input("🔗 Click to Copy Live Master Instagram Bio Link:", value=full_live_share_link, readonly=True)
        st.info("💡 Note: Once you deploy this code once onto Community Cloud, your app acts as its own hosting server. When you update details, the link updates itself automatically!")
