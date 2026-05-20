import streamlit as st

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
# 📡 TRACK 1: THE POP-UP VIEW (When a user clicks your single Instagram link)
# ==============================================================================
try:
    current_params = st.query_params
except Exception:
    current_params = {}

# If "user" is in the URL, hide the creator dashboard and just show the 3 links!
if "user" in current_params:
    target_user = current_params["user"]
    user_bio = current_params.get("bio", "Welcome to my link hub!")
    
    # Safely extract your 3 titles and URLs
    raw_titles = current_params.get_all("t") if hasattr(current_params, "get_all") else current_params.get("t", [])
    raw_urls = current_params.get_all("u") if hasattr(current_params, "get_all") else current_params.get("u", [])
    
    if isinstance(raw_titles, str): raw_titles = [raw_titles]
    if isinstance(raw_urls, str): raw_urls = [raw_urls]
    
    # Render the beautiful smartphone page layout for visitors
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
        st.caption("No links found.")
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ==============================================================================
# ⚙️ TRACK 2: THE CREATOR PANEL (Where you build it)
# ==============================================================================
if "builder_links" not in st.session_state:
    st.session_state.builder_links = [
        {"title": "📱 Clinic Web App", "url": "https://your-clinic-app.streamlit.app"},
        {"title": "🧮 JS Calculator", "url": "https://your-username.github.io/calculator"},
        {"title": "💻 GitHub Profile", "url": "https://github.com"}
    ]

st.title("🔮 The 3-in-1 Master Link Hub")
st.caption("Pack multiple apps into one single link for your Instagram bio.")
st.markdown("---")

left_col, right_col = st.columns([1.1, 1.3], gap="large")

with left_col:
    st.subheader("📱 Live Preview")
    c_user = st.text_input("Username:", value="dilshad.dev")
    c_bio = st.text_input("Short Bio:", value="My Portfolio & Live Applications")
    
    st.markdown('<div class="phone-view">', unsafe_allow_html=True)
    st.markdown('<div class="avatar-icon">🤖</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>@{c_user}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #94a3b8; font-size:13px;">{c_bio}</p>', unsafe_allow_html=True)
    st.markdown('<div style="border-bottom: 1px solid #1e293b; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
    
    for item in st.session_state.builder_links:
        st.markdown(f'<div class="bio-link">{item["title"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.subheader("🛠️ Manage Your Links")
    
    with st.container(border=True):
        st.markdown("#### ➕ Add a New App Link")
        t_input = st.text_input("App Name / Label:", placeholder="e.g., My Clinic App")
        u_input = st.text_input("App URL:", placeholder="https://...")
        
        if st.button("Add Link", use_container_width=True):
            if t_input and u_input:
                st.session_state.builder_links.append({"title": t_input, "url": u_input})
                st.rerun()
                
    with st.container(border=True):
        st.markdown("#### 📋 Current Combined Links")
        for idx, item in enumerate(st.session_state.builder_links):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{item['title']}** → {item['url']}")
            with col_b:
                if st.button("Delete", key=f"del_{idx}", use_container_width=True):
                    st.session_state.builder_links.pop(idx)
                    st.rerun()

    # ==============================================================================
    # 🔗 THE MASTER LINK GENERATOR
    # ==============================================================================
    with st.container(border=True):
        st.markdown("#### 🚀 BOOM! Your Combined Link is Ready")
        st.caption("Paste your live Streamlit main URL below once, and it will instantly give you the magic link.")
        
        # Simply paste your deployed app URL here, like: https://yourname-hub.streamlit.app/
        my_live_url = st.text_input("1. Paste your deployed Streamlit URL here:", value="https://your-app-name.streamlit.app/")
        
        # Ensure trailing slash
        if not my_live_url.endswith("/"):
            my_live_url += "/"
            
        # Compile query strings instantly
        url_arguments = f"?user={c_user}&bio={c_bio.replace(' ', '+')}"
        for item in st.session_state.builder_links:
            url_arguments += f"&t={item['title'].replace(' ', '+')}&u={item['url']}"
            
        full_live_share_link = my_live_url + url_arguments
        
        st.markdown("**2. Copy this master link and put it on Instagram:**")
        st.text_area("Your Magic Link:", value=full_live_share_link, height=100, disabled=True)
