import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import random
from datetime import datetime, timedelta
import io

# ==============================================================================
# 🎨 ENTERPRISE CODEBASE CONFIGURATION ARCHITECTURE
# ==============================================================================
st.set_page_config(
    page_title="InstaGrid OS Premium | The Creator Workspace",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔒 MASTER CLASS PRO SYSTEM GLASSMORPHIC STYLING MATRIX
pro_css = """
<style>
/* Global Canvas Deep Dark Background Realignment */
div[data-testid="stAppViewContainer"], .main {
    background: radial-gradient(circle at top left, #05070f, #02040a, #000000) !important;
}

/* Sidebar Custom Tech Adjustments */
div[data-testid="stSidebar"] {
    background-color: #04060e !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Typography Color Injections */
h1, h2, h3, h4, h5, h6, .phone-frame p, .phone-frame span, div[data-testid="stMarkdownContainer"] p {
    color: #f1f5f9 !important;
    font-family: system-ui, -apple-system, sans-serif !important;
}

/* Elite Smartphone Mock Wrapper Layout */
.phone-frame {
    background: #020306;
    padding: 26px;
    border-radius: 42px;
    border: 3px solid rgba(255, 255, 255, 0.07);
    box-shadow: 0 40px 80px rgba(0, 0, 0, 0.95), 0 0 40px rgba(6, 182, 212, 0.05);
    max-width: 440px;
    margin: 0 auto;
    position: relative;
}

.insta-badge {
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    color: white;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(220, 39, 67, 0.3);
}

/* Live Simulation Overlay Metrics Badges */
.metric-pill-box {
    background: rgba(9, 13, 24, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 6px 10px;
    margin-top: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: #94a3b8;
}
.metric-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.text-heart { color: #f43f5e; text-shadow: 0 0 8px rgba(244, 63, 94, 0.4); }
.text-comment { color: #38bdf8; text-shadow: 0 0 8px rgba(56, 189, 248, 0.4); }
.text-share { color: #10b981; text-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }

/* Analytical Scoring Board Components */
.score-card {
    background: rgba(6, 182, 212, 0.03);
    border: 1px solid rgba(6, 182, 212, 0.15);
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 16px;
    text-align: center;
}
.score-value {
    font-size: 32px;
    font-weight: 900;
    color: #06b6d4;
    text-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
}

/* Custom Hashtag Badges Layout handles */
.tag-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #818cf8;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    margin: 3px;
}
</style>
"""
st.markdown(pro_css, unsafe_allow_html=True)

# ==============================================================================
# 📊 DEEP TRENDING DICTIONARY MODEL & HOOK FRAMES
# ==============================================================================
TRENDING_MARKET_DATABASE = {
    "Tech & Coding": [
        {"tag": "#buildinpublic", "tier": "Niche/High-Eng", "volume": "2.4M", "weight": 0.98, "status": "🚀 HIGH VELOCITY"},
        {"tag": "#solopreneur", "tier": "Core-Industry", "volume": "1.8M", "weight": 0.94, "status": "🔥 BURSTING"},
        {"tag": "#pythonprogramming", "tier": "Broad-Mass", "volume": "5.2M", "weight": 0.89, "status": "STABLE"},
        {"tag": "#uidesign", "tier": "Core-Industry", "volume": "3.1M", "weight": 0.85, "status": "RISING"},
        {"tag": "#developerlife", "tier": "Broad-Mass", "volume": "8.7M", "weight": 0.91, "status": "🔥 BURSTING"}
    ],
    "Business & SaaS": [
        {"tag": "#saasfounder", "tier": "Niche/High-Eng", "volume": "840K", "weight": 0.99, "status": "🚀 EXPONENTIAL"},
        {"tag": "#indiehackers", "tier": "Niche/High-Eng", "volume": "1.1M", "weight": 0.96, "status": "🚀 EXPONENTIAL"},
        {"tag": "#growthhacking", "tier": "Core-Industry", "volume": "4.3M", "weight": 0.91, "status": "🔥 BURSTING"},
        {"tag": "#mvp", "tier": "Niche/High-Eng", "volume": "650K", "weight": 0.87, "status": "RISING"},
        {"tag": "#bootstrap", "tier": "Broad-Mass", "volume": "920K", "weight": 0.82, "status": "STABLE"}
    ],
    "Local Service Shop": [
        {"tag": "#acrepair", "tier": "Niche/High-Eng", "volume": "320K", "weight": 0.97, "status": "🚀 HIGH LOCAL DEMAND"},
        {"tag": "#hvacmechanic", "tier": "Core-Industry", "volume": "540K", "weight": 0.93, "status": "🔥 BURSTING"},
        {"tag": "#airconditioning", "volume": "2.1M", "tier": "Broad-Mass", "weight": 0.84, "status": "STABLE"},
        {"tag": "#smallbusinessindia", "tier": "Broad-Mass", "volume": "1.5M", "weight": 0.92, "status": "🚀 RISING"},
        {"tag": "#maintenance", "tier": "Broad-Mass", "volume": "4.6M", "weight": 0.79, "status": "STABLE"}
    ]
}

HOOK_TEMPLATES = {
    "Founder-Vibe": [
        "I built this utility script in 4 hours. It solves a problem hurting thousands.",
        "Stop building complicated frameworks. The simple micro-SaaS layers win.",
        "Day {day} of building in public. Here is the raw data most founders hide."
    ],
    "Scientific/Analytical": [
        "The algorithmic logic behind this specific layout design is simple.",
        "Data Analysis: Why {metric}% of local service pipelines break in summer.",
        "An objective breakdown of how we optimized this engineering workflow."
    ],
    "Aggressive/High-Energy": [
        "Stop wasting execution cycles on things that do not move numbers.",
        "This is the exact strategy being used to dominate local market segments.",
        "If your code isn't running automated tasks for you today, you're losing ground."
    ],
    "Minimal/Clean": [
        "Focus on pure utility.",
        "Refining the base infrastructure.",
        "Clean logic, scalable outcomes."
    ]
}

# ==============================================================================
# 🧠 RUNTIME SESSION STATE MEMORY MASTER ENGINE
# ==============================================================================
if "grid_images" not in st.session_state:
    st.session_state.grid_images = []
if "original_images" not in st.session_state:
    st.session_state.original_images = []  # Backup for rolling back raw images
if "content_metadata" not in st.session_state:
    st.session_state.content_metadata = {}
if "global_followers" not in st.session_state:
    st.session_state.global_followers = 18400

# --- CORE APP BANNER HEADLINE ---
st.title("🔮 InstaGrid OS Premium")
st.caption("The Next-Gen Full-Stack Content Operating System & Algorithmic Simulator • Engineered by Dilshad")
st.markdown("---")

# ==============================================================================
# 🎛️ SIDEBAR CONTROL FRAMEWORK SECTION
# ==============================================================================
with st.sidebar:
    st.markdown("### 🧬 Global Audience Profile")
    st.session_state.global_followers = st.number_input(
        "Base Follower Metrics Vector:", 
        min_value=100, 
        max_value=10000000, 
        value=st.session_state.global_followers, 
        step=500
    )
    
    st.markdown("---")
    st.markdown("### 🎨 Sandbox Image FX Filter Engine")
    st.caption("Apply real-time high-performance pixel operations directly onto your layout files.")
    
    active_filter = st.selectbox(
        "Select Matrix Transformation Layer:",
        options=["None/Raw Matrix", "Deep Cyber Greyscale", "High-Contrast Neon", "Warm Amber Tone", "Inverted Negative Mask"]
    )
    
    contrast_val = st.slider("Enhance Intensity Scale:", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    
    st.markdown("---")
    st.markdown("### 🗃️ Bulk Processing Systems")
    if st.button("⚡ Trigger Mock Metric Initialization", use_container_width=True):
        for idx in range(len(st.session_state.grid_images)):
            if idx in st.session_state.content_metadata:
                st.session_state.content_metadata[idx]["likes"] = random.randint(1500, 8500)
                st.session_state.content_metadata[idx]["comments"] = random.randint(120, 950)
                st.session_state.content_metadata[idx]["shares"] = random.randint(90, 480)
        st.toast("Simulated metrics array updated!", icon="🔥")
        st.rerun()

# Apply Real-Time Image Filter Matrix Pipeline adjustments
def apply_image_effects(img, filter_type, enhancement):
    # Ensure working copy is in full RGB
    working_img = img.copy().convert("RGB")
    
    if filter_type == "Deep Cyber Greyscale":
        working_img = ImageOps.grayscale(working_img).convert("RGB")
    elif filter_type == "High-Contrast Neon":
        working_img = ImageOps.autocontrast(working_img)
    elif filter_type == "Warm Amber Tone":
        # Python Matrix multiplication simulation loop for amber photo warmths
        r, g, b = working_img.split()
        r = r.point(lambda i: i * 1.1)
        b = b.point(lambda i: i * 0.8)
        working_img = Image.merge("RGB", (r, g, b))
    elif filter_type == "Inverted Negative Mask":
        working_img = ImageOps.invert(working_img)
        
    if enhancement != 1.0:
        enhancer = ImageEnhance.Contrast(working_img)
        working_img = enhancer.enhance(enhancement)
        
    return working_img

# Sync current image arrays with selected filters
processed_grid_images = []
for original_img in st.session_state.original_images:
    processed_grid_images.append(apply_image_effects(original_img, active_filter, contrast_val))
st.session_state.grid_images = processed_grid_images

# ==============================================================================
# 📊 MASTER STRUCTURAL WORKSPACE LAYOUT ROW
# ==============================================================================
workspace_left, workspace_right = st.columns([1.1, 1.3], gap="large")

# ==============================================================================
# 📱 LEFT COLUMN: THE INTUITIVE MOCK PREVIEW SIMULATOR
# ==============================================================================
with workspace_left:
    st.subheader("📱 Immersive Virtual Sandbox Device")
    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)
    
    # Mock Smartphone Header Interface Matrix Components
    hdr_1, hdr_2 = st.columns([3, 1])
    with hdr_1:
        st.markdown('### **dilshad.dev** <span class="insta-badge">CREATOR OS</span>', unsafe_allow_html=True)
    with hdr_2:
        grid_borders = st.toggle("Grid Lines", value=True)
        
    av_col, stat_col = st.columns([1, 4])
    with av_col:
        st.markdown("🤖")
    with stat_col:
        st.markdown(f"**{len(st.session_state.grid_images)}** posts &nbsp;•&nbsp; **{st.session_state.global_followers:,}** followers &nbsp;•&nbsp; **512** following")
        
    st.markdown("**Dilshad | Product Engineer**")
    st.caption("Building high-utility software products and automated SaaS infrastructure layers.")
    st.markdown("---")
    
    # Interactive Image Matrix Rendering System Loop
    if st.session_state.grid_images:
        for row_idx in range(0, len(st.session_state.grid_images), 3):
            row_slice = st.session_state.grid_images[row_idx:row_idx+3]
            grid_cols = st.columns(3, gap="small" if grid_borders else "none")
            
            for col_idx, img_obj in enumerate(row_slice):
                global_index = row_idx + col_idx
                
                # Lazy setup verification tracking for active element dictionaries
                if global_index not in st.session_state.content_metadata:
                    st.session_state.content_metadata[global_index] = {
                        "caption": "Building fresh production tools for the ecosystem workflow loop.", 
                        "date": datetime.today() + timedelta(days=global_index), 
                        "likes": random.randint(240, 1150),
                        "comments": random.randint(18, 142), 
                        "shares": random.randint(8, 76),
                        "tags_selected": []
                    }
                
                meta = st.session_state.content_metadata[global_index]
                
                with grid_cols[col_idx]:
                    st.image(img_obj, use_container_width=True)
                    
                    # HTML injection structure rendering metrics overlay panels
                    metric_html = f"""
                    <div class="metric-pill-box">
                        <span class="metric-item"><span class="text-heart">❤️</span> {meta['likes']}</span>
                        <span class="metric-item"><span class="text-comment">💬</span> {meta['comments']}</span>
                        <span class="metric-item"><span class="text-share">✈️</span> {meta['shares']}</span>
                    </div>
                    <center><code style='color:#475569; font-size:10px;'>Slot {global_index}</code></center>
                    """
                    st.markdown(metric_html, unsafe_allow_html=True)
    else:
        st.info("💡 Load your image files inside the Control Deck panel to boot the visualization matrix.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# ⚙️ RIGHT COLUMN: CREATIVE OPTIMIZATION & MACHINE LEARNING ANALYTICS DECKS
# ==============================================================================
with workspace_right:
    st.subheader("⚙️ Mission Control Center Panel")
    
    # SYSTEM CORE CONTAINER 1: FILE INGESTION PIPELINE
    with st.container(border=True):
        st.markdown("#### 📁 Core Resource Asset Pipeline Ingestion")
        uploaded_files = st.file_uploader(
            "Upload configuration image files to pass into the system memory bank:", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="master_system_uploader"
        )
        if uploaded_files:
            raw_images_list = [Image.open(f) for f in uploaded_files]
            st.session_state.original_images = raw_images_list
            # Immediate operational pass sync
            st.session_state.grid_images = [apply_image_effects(img, active_filter, contrast_val) for img in raw_images_list]
            
        if st.button("🗑️ Purge Active Media System Memory Canvas", use_container_width=True):
            st.session_state.grid_images = []
            st.session_state.original_images = []
            st.session_state.content_metadata = {}
            st.rerun()

    # SYSTEM CORE CONTAINER 2: THE METRIC CONSOLE & WRITING MATRIX
    if st.session_state.grid_images:
        with st.container(border=True):
            st.markdown("#### 🛠️ Deep Performance Tuning & Architectural Matrix Control")
            edit_slot = st.selectbox("Choose a target layout viewport slot to optimize:", options=range(len(st.session_state.grid_images)))
            
            current_meta = st.session_state.content_metadata[edit_slot]
            
            # --- VIRALITY INDEX ADVANCED COMPUTER EQUATION MODEL ---
            likes_score = current_meta["likes"]
            comments_score = current_meta["comments"]
            shares_score = current_meta["shares"]
            followers_pool = st.session_state.global_followers
            
            # Algorithmic Virality Score Logic
            virality_index = ((likes_score * 1.0) + (comments_score * 4.0) + (shares_score * 7.0)) / followers_pool * 100
            
            col_v1, col_v2 = st.columns([1.5, 2.5])
            with col_v1:
                st.markdown(f"""
                <div class="score-card">
                    <p style="margin:0; font-size:11px; color:#94a3b8; letter-spacing:1px;">ALGORITHMIC VIRALITY SCORE</p>
                    <div class="score-value">{virality_index:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col_v2:
                if virality_index > 15.0:
                    st.success("🚀 HIGH PROBABILITY VELOCITY: This engagement ratio is projected to clear system algorithmic loops easily.")
                elif virality_index > 5.0:
                    st.warning("⚡ STABLE OUTCOME MATRIX: Standard visibility projection. Boost comment loops or share triggers to expand reach.")
                else:
                    st.error("📉 SATURATED REACH RATIO: High friction rate. Redesign copy vectors or call-to-action metrics.")

            # Metric Dial Controls
            st.markdown("##### 📊 Real-Time Engagement Adjusters")
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                custom_likes = st.number_input("Adjust Likes:", min_value=0, value=int(current_meta["likes"]), key=f"lk_v2_{edit_slot}")
            with m_col2:
                custom_comments = st.number_input("Adjust Comments:", min_value=0, value=int(current_meta["comments"]), key=f"cm_v2_{edit_slot}")
            with m_col3:
                custom_shares = st.number_input("Adjust Shares:", min_value=0, value=int(current_meta["shares"]), key=f"sh_v2_{edit_slot}")

            st.markdown("---")
            
            # --- PRO EXCLUSIVE FEATURE: COGNITIVE AI COPYWRITING TOOL ENGINE ---
            st.markdown("##### 🧠 Context-Aware Copy Hook Generation Matrix")
            st.caption("Auto-inject high-converting text hooks mapped directly to psychology profiles.")
            
            tone_selection = st.selectbox("Select Target Campaign Voice Profile Tone:", options=list(HOOK_TEMPLATES.keys()))
            
            if st.button("⚡ Generate and Inject High-Converting Hook Variant", use_container_width=True):
                suggested_hook = random.choice(HOOK_TEMPLATES[tone_selection])
                if "{day}" in suggested_hook:
                    suggested_hook = suggested_hook.format(day=edit_slot+1)
                if "{metric}" in suggested_hook:
                    suggested_hook = suggested_hook.format(metric=random.randint(65, 94))
                    
                # Prepend or overwrite current text string setup
                current_meta["caption"] = f"{suggested_hook}\n\n{current_meta['caption']}"
                st.session_state.content_metadata[edit_slot]["caption"] = current_meta["caption"]
                st.rerun()

            caption_text = st.text_area("Draft Campaign Caption Text:", value=current_meta["caption"], height=120, key=f"cap_v2_{edit_slot}")
            st.caption(f"✍️ Data Density Counter: `{len(caption_text)}` / 2200 maximum safe characters.")

            st.markdown("---")
            
            # --- ADVANCED BALANCED HASHTAG CALCULATOR HUB ---
            st.markdown("##### 📈 Real-Time Trending Hashtag Optimization Engine")
            selected_niche = st.selectbox("Select Campaign Target Segment Focus:", options=list(TRENDING_MARKET_DATABASE.keys()))
            
            niche_tags = TRENDING_MARKET_DATABASE[selected_niche]
            
            st.markdown("*Click on high-performance tag records below to instantly append them into the production engine copy:*")
            
            for data_block in niche_tags:
                col_t1, col_t2, col_t3 = st.columns([2, 1, 1.5])
                with col_t1:
                    if st.button(f"➕ {data_block['tag']}", key=f"btn_v2_{edit_slot}_{data_block['tag']}", use_container_width=True):
                        if data_block['tag'] not in caption_text:
                            caption_text += f" {data_block['tag']}"
                            st.session_state.content_metadata[edit_slot]["caption"] = caption_text
                            st.rerun()
                with col_t2:
                    st.markdown(f"`{data_block['volume']}`")
                with col_t3:
                    st.markdown(f"<span class='tag-badge'>{data_block['tier']}</span>", unsafe_allow_html=True)

            st.markdown("---")
            schedule_date = st.date_input("Target Post Deployment Date Target Window:", value=current_meta["date"], key=f"dt_v2_{edit_slot}")
            
            # Update values back into global state tracking registers
            st.session_state.content_metadata[edit_slot] = {
                "caption": caption_text,
                "date": schedule_date,
                "likes": custom_likes,
                "comments": custom_comments,
                "shares": custom_shares
            }

            # --- SYSTEM CORE CONTAINER 3: EXPORT ENGINE ARCHITECTURE ---
            st.markdown("---")
            st.markdown("#### 📡 Strategy Data Packet Blueprint Export Summary")
            
            final_strategy_manifest = f"""=== INSTAGRID CREATOR OS EXPORT PACKAGE ===
DEPLOYMENT TIMELINE TARGET: {schedule_date}
ESTIMATED VIRALITY PROJECTION SCORE: {virality_index:.2f}%
TARGET INTERACTION PARAMETERS:
- Likes: {custom_likes}
- Comments: {custom_comments}
- Shares: {custom_shares}

FINAL COPY TEXT MANIFEST SUMMARY:
{caption_text}
==========================================="""
            
            st.code(final_strategy_manifest, language="text")
            
            st.download_button(
                label="💾 Export Content Manifest Package Details (.txt)",
                data=final_strategy_manifest,
                file_name=f"instagrid_deployment_manifest_slot_{edit_slot}.txt",
                mime="text/plain",
                use_container_width=True
            )

    # REORDERING TIMELINE ARRAY ENGINE TOOL PANEL
    if len(st.session_state.grid_images) > 1:
        with st.container(border=True):
            st.markdown("#### 🔄 Sequence Timeline Re-Order Tool")
            sel_idx = st.number_input("Select target slot index to shift:", min_value=0, max_value=len(st.session_state.grid_images)-1, step=1, value=0, key="v2_reorder_target")
            target_pos = st.slider("Drag target slot to its new lane index placement:", min_value=0, max_value=len(st.session_state.grid_images)-1, value=int(sel_idx), key="v2_reorder_slider")
            
            if st.button("Apply New Timeline Order", use_container_width=True, key="v2_reorder_action"):
                # Move image inside both lists synchronously to keep filter cache from exploding
                popped_img = st.session_state.grid_images.pop(sel_idx)
                st.session_state.grid_images.insert(target_pos, popped_img)
                
                popped_orig = st.session_state.original_images.pop(sel_idx)
                st.session_state.original_images.insert(target_pos, popped_orig)
                
                # Re-index data mappings cleanly 
                popped_meta = st.session_state.content_metadata.pop(sel_idx, None)
                if popped_meta:
                    st.session_state.content_metadata[target_pos] = popped_meta
                    
                st.toast("Timeline array re-indexed successfully!", icon="✅")
                st.rerun()
