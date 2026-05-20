import streamlit as st
import io

# Page Config Matrix
st.set_page_config(
    page_title="BioLink Forge Pro | Instagram Creator Engine",
    page_icon="🔮",
    layout="wide"
)

# Clean, professional background styling for the Streamlit deck
st.markdown("""
<style>
div[data-testid="stAppViewContainer"], .main {
    background: #090d16 !important;
}
h1, h2, h3, h4, p, span, label {
    color: #f8fafc !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}
.phone-preview-container {
    background: #020617;
    padding: 30px 20px;
    border-radius: 36px;
    border: 3px solid #1e293b;
    max-width: 380px;
    margin: 0 auto;
    text-align: center;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
.preview-avatar {
    width: 90px;
    height: 90px;
    background: linear-gradient(45deg, #f09433, #dc2743, #cc2366);
    border-radius: 50%;
    margin: 0 auto 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: white;
}
.preview-link-card {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    color: #ffffff !important;
    text-decoration: none;
    display: block;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.2s;
}
</style>
""", unsafe_allow_html=True)

# App Memory State Allocation
if "links_list" not in st.session_state:
    st.session_state.links_list = [
        {"title": "💻 Explore My GitHub Portfolio", "url": "https://github.com/"},
        {"title": "🚀 Check Out My Active SaaS Apps", "url": "https://streamlit.io"},
    ]

st.title("🔮 BioLink Forge Pro")
st.caption("Build, Simulate, and Export Custom High-Converting Instagram Bio-Link Landing Pages • Engineered by Dilshad")
st.markdown("---")

# Main Page Split Horizontal Columns
preview_col, engine_col = st.columns([1.1, 1.3], gap="large")

# ==============================================================================
# 📱 LEFT SIDE: LIVE SMARTPHONE PORTFOLIO PREVIEW
# ==============================================================================
with preview_col:
    st.subheader("📱 Live Mobile Preview")
    
    # User Input Collection Handles from Sidebar / Controls
    username = st.text_input("Profile Display Handle:", value="dilshad.dev", max_chars=30)
    bio_text = st.text_area("Profile Short Bio Text:", value="Building premium web apps and utility micro-SaaS layers.", max_chars=120)
    theme_color = st.color_picker("Pick Link Highlight Color:", value="#06b6d4")
    
    st.markdown('<div class="phone-preview-container">', unsafe_allow_html=True)
    
    # Simulated Device Header Elements
    st.markdown(f'<div class="preview-avatar">🚀</div>', unsafe_allow_html=True)
    st.markdown(f'<h3>@{username}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #94a3b8; font-size:13px; margin-bottom:20px;">{bio_text}</p>', unsafe_allow_html=True)
    st.markdown('<div style="border-bottom: 1px solid #1e293b; margin-bottom:20px;"></div>', unsafe_allow_html=True)
    
    # Loop over active state lists and draw links interactively inside the preview
    for item in st.session_state.links_list:
        link_html = f"""
        <a class="preview-link-card" style="border-left: 4px solid {theme_color};" href="{item['url']}" target="_blank">
            {item['title']}
        </a>
        """
        st.markdown(link_html, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# ⚙️ RIGHT SIDE: LINK LOGIC MANAGEMENT & CLEAN HTML COMPILING
# ==============================================================================
with engine_col:
    st.subheader("⚙️ Link Array Engine & Exporter")
    
    # Add link block section handles
    with st.container(border=True):
        st.markdown("#### ➕ Append Fresh Target Link Asset")
        new_title = st.text_input("Button Link Title Text:", placeholder="e.g., 🛠️ Hire Me On Freelance Link")
        new_url = st.text_input("Destination URL Target Link:", placeholder="https://yourwebsite.com")
        
        if st.button("Inject Link Node Into Matrix", use_container_width=True):
            if new_title and new_url:
                st.session_state.links_list.append({"title": new_title, "url": new_url})
                st.toast("Link layout array updated locally!", icon="✅")
                st.rerun()
            else:
                st.error("Please fill out both Title and URL fields.")

    # Current links display database view tracking modules
    with st.container(border=True):
        st.markdown("#### 📋 Active Link Register Management")
        if st.session_state.links_list:
            for idx, item in enumerate(st.session_state.links_list):
                r_col1, r_col2 = st.columns([3, 1])
                with r_col1:
                    st.markdown(f"`Slot {idx}`: **{item['title']}** → *{item['url']}*")
                with r_col2:
                    if st.button("🗑️ Purge", key=f"del_{idx}", use_container_width=True):
                        st.session_state.links_list.pop(idx)
                        st.rerun()
        else:
            st.info("No active redirection links configured. Add one above to populate.")

    # ==============================================================================
    # 💾 CORE COMPILER ENGINE: EXPORT TO PURE HTML/CSS FILE
    # ==============================================================================
    with st.container(border=True):
        st.markdown("#### 🏁 Compile Production Code Packet")
        st.caption("Generate clean, standalone, highly performant responsive HTML code you can upload directly to GitHub Pages for your Instagram bio link.")
        
        # Build dynamic HTML link strings
        generated_html_links = ""
        for item in st.session_state.links_list:
            generated_html_links += f'\n        <a class="link-btn" href="{item["url"]}" target="_blank">{item["title"]}</a>'
            
        # Complete standalone production template layout
        raw_production_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@{username} | My Link Bio Hub</title>
    <style>
        body {{
            background: radial-gradient(circle at top, #0f172a, #020617);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }}
        .container {{
            width: 100%;
            max-width: 400px;
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 35px 25px;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }}
        .avatar {{
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #f09433, #dc2743, #cc2366);
            border-radius: 50%;
            margin: 0 auto 15px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
        }}
        h1 {{
            font-size: 20px;
            margin: 10px 0 5px 0;
            letter-spacing: -0.5px;
        }}
        .bio {{
            font-size: 14px;
            color: #94a3b8;
            line-height: 1.5;
            margin-bottom: 25px;
        }}
        .link-btn {{
            display: block;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 5px solid {theme_color};
            color: #ffffff;
            text-decoration: none;
            padding: 14px;
            margin: 12px 0;
            border-radius: 12px;
            font-weight: 500;
            font-size: 15px;
            transition: transform 0.2s, background 0.2s;
        }}
        .link-btn:hover {{
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="avatar">🚀</div>
        <h1>@{username}</h1>
        <div class="bio">{bio_text}</div>
        <div style="border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px;"></div>
        {generated_html_links}
    </div>
</body>
</html>
"""

        st.code(raw_production_html[:400] + "\n... [Code compiled successfully] ...", language="html")
        
        # Binary I/O extraction loop wrapper
        html_bytes = io.BytesIO(raw_production_html.encode('utf-8'))
        
        st.download_button(
            label="📥 Download Production index.html Web Bundle",
            data=html_bytes,
            file_name="index.html",
            mime="text/html",
            use_container_width=True
        )
