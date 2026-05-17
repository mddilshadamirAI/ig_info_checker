import streamlit as st
from PIL import Image
import random

# 🎨 Page Configuration & Layout Customizing Engine
st.set_page_config(
    page_title="InstaGrid Studio Pro | Content Planner",
    page_icon="🔮",
    layout="wide"
)

# 🔒 TRIPLE-GUARDED PRO CSS: Specifically shields internal widgets from text overlaps
pro_css = """
<style>
/* 1. Global App Deep Dark Canvas Background */
div[data-testid="stAppViewContainer"], .main {
    background: radial-gradient(circle at top left, #1e1b4b, #0b0f19, #020617) !important;
}

/* 2. Target Text ONLY within explicit markdown segments, headers, or our phone frame */
h1, h2, h3, h4, .phone-frame p, .phone-frame span, div[data-testid="stMarkdownContainer"] p {
    color: #f1f5f9 !important;
    font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* 3. CRITICAL BUG FIX: Reset Streamlit file uploader native button text properties to default */
div[data-testid="stFileUploader"] button {
    color: inherit !important;
}
div[data-testid="stFileUploaderDropzone"] div {
    color: #94a3b8 !important;
}

/* 4. Glassmorphism Profile Frame Layout */
.phone-frame {
    background: #090d16;
    padding: 24px;
    border-radius: 36px;
    border: 2px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
    max-width: 410px;
    margin: 0 auto;
}
.insta-badge {
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    color: white;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: bold;
}
</style>
"""
st.markdown(pro_css, unsafe_allow_html=True)

# Pre-programmed Hashtag Pools for the Mix Engine Tool
HASHTAG_POOLS = {
    "Tech & Coding": ["#developer", "#programming", "#codinglife", "#javascript", "#python", "#webdev", "#softwareengineering", "#buildinpublic", "#uidesign"],
    "Business & SaaS": ["#entrepreneur", "#saas", "#solopreneur", "#indiehackers", "#marketingtips", "#growthhacking", "#startup", "#founder", "#businessowner"],
    "Local Service Shop": ["#acrepair", "#hvac", "#localservice", "#airconditioning", "#maintenance", "#homeservice", "#smallbusiness", "#supportlocal"]
}

# App Core Memory Framework
if "grid_images" not in st.session_state:
    st.session_state.grid_images = []
if "content_metadata" not in st.session_state:
    st.session_state.content_metadata = {}

# --- MAIN PAGE HEADLINE ---
st.title("🔮 InstaGrid Studio Pro")
st.caption("The Premium Content Organizer & Feed Visualization Suite • Engineered by Dilshad")
st.markdown("---")

# Split the Workspace into Two Clean Master Horizontal Structural Lanes
workspace_left, workspace_right = st.columns([1.1, 1.3], gap="large")

# ==============================================================================
# 📱 LEFT COLUMN: THE REALISTIC PHONE PREVIEW CANVAS
# ==============================================================================
with workspace_left:
    st.subheader("📱 Feed Viewport Layout")
    
    # Render Interactive Phone Frame Wrapper Container Block
    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)
    
    # Mock Instagram Top Row Title Header Layout
    hdr_1, hdr_2 = st.columns([3, 1])
    with hdr_1:
        st.markdown('### **dilshad.dev** <span class="insta-badge">PRO</span>', unsafe_allow_html=True)
    with hdr_2:
        grid_lines = st.toggle("Grid Borders", value=True)
        
    # Profile Sub-Header Statistics Grid Row Block Elements
    av_col, stat_col = st.columns([1, 3])
    with av_col:
        st.markdown("⚡")
    with stat_col:
        post_count = len(st.session_state.grid_images)
        st.markdown(f"**{post_count}** posts &nbsp;&nbsp;•&nbsp;&nbsp; **18.4K** followers &nbsp;&nbsp;•&nbsp;&nbsp; **512** following")
    
    st.markdown("**Dilshad | Product Engineer**")
    st.caption("Building utility micro-SaaS layers for high-performance creative workflows.")
    st.markdown("---")
    
    # Render Interactive Image Matrix System
    if st.session_state.grid_images:
        for row_idx in range(0, len(st.session_state.grid_images), 3):
            row_slice = st.session_state.grid_images[row_idx:row_idx+3]
            grid_cols = st.columns(3, gap="small" if grid_lines else "none")
            
            for col_idx, img_obj in enumerate(row_slice):
                global_index = row_idx + col_idx
                with grid_cols[col_idx]:
                    st.image(img_obj, use_container_width=True)
                    st.markdown(f"<center><code style='color:#64748b;'>Slot {global_index}</code></center>", unsafe_allow_html=True)
    else:
        st.info("💡 Use the Control Deck panel to dump creative photo assets here.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# ⚙️ RIGHT COLUMN: THE CREATIVE PRODUCTION ENGINE
# ==============================================================================
with workspace_right:
    st.subheader("⚙️ Studio Control Deck")
    
    # SECTION 1: ASSET MANAGEMENT CARD FRAME PANEL LINK
    with st.container(border=True):
        st.markdown("#### 📁 Media Resource Ingestion")
        uploaded_files = st.file_uploader(
            "Drop your visual composition files here:", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="studio_uploader"
        )
        
        if uploaded_files:
            new_list = []
            for f in uploaded_files:
                new_list.append(Image.open(f))
            st.session_state.grid_images = new_list
            
        if st.button("🗑️ Reset Media Canvas", use_container_width=True):
            st.session_state.grid_images = []
            st.session_state.content_metadata = {}
            st.rerun()

    # SECTION 2: INTERACTIVE TIME-AXIS REORDER ENGINE MAPPING BLOCK
    if len(st.session_state.grid_images) > 1:
        with st.container(border=True):
            st.markdown("#### 🔄 Sequence Timeline Re-Order Tool")
            sel_idx = st.number_input("Select target slot index to shift:", min_value=0, max_value=len(st.session_state.grid_images)-1, step=1, value=0)
            target_pos = st.slider("Drag target slot to its new lane index placement:", min_value=0, max_value=len(st.session_state.grid_images)-1, value=int(sel_idx))
            
            if st.button("Apply New Timeline Order", use_container_width=True):
                popped_card = st.session_state.grid_images.pop(sel_idx)
                st.session_state.grid_images.insert(target_pos, popped_card)
                st.toast("Timeline array re-indexed successfully!", icon="✅")
                st.rerun()

    # SECTION 3: WORKSPACE SCHEDULER & HASHTAG GENERATOR META ENGINE PANEL
    if st.session_state.grid_images:
        with st.container(border=True):
            st.markdown("#### 📝 Metadata Architect & Copywriter Hub")
            edit_slot = st.selectbox("Choose a layout slot to write copy for:", options=range(len(st.session_state.grid_images)))
            
            # Initialize slot dictionary memories
            if edit_slot not in st.session_state.content_metadata:
                st.session_state.content_metadata[edit_slot] = {"caption": "", "date": None, "hashtags": ""}
            
            current_meta = st.session_state.content_metadata[edit_slot]
            
            # Smart Copywriting Features Inputs
            caption_text = st.text_area("Draft Instagram Caption Copy text:", value=current_meta["caption"], height=100)
            st.caption(f"✍️ Character Length Tracker: `{len(caption_text)}` characters (Instagram Maximum Limit boundary: 2200)")
            
            # Interactive Smart AI Hashtag Builder Injection Selector Array
            niche_choice = st.selectbox("Select Target Campaign Niche Audience:", options=["None"] + list(HASHTAG_POOLS.keys()))
            if niche_choice != "None" and st.button("⚡ Inject Optimized Hashtag Mix"):
                chosen_pool = HASHTAG_POOLS[niche_choice]
                random_sample = random.sample(chosen_pool, min(len(chosen_pool), 5))
                generated_string = " " + " ".join(random_sample)
                caption_text += generated_string
                st.rerun()
                
            schedule_date = st.date_input("Target Post Deployment Date Target line:", value=current_meta["date"])
            
            # Save local changes
            st.session_state.content_metadata[edit_slot] = {
                "caption": caption_text,
                "date": schedule_date,
                "hashtags": ""
            }
            
            # Complete Output Export View Summary Card Module Display
            st.markdown("---")
            st.markdown(f"📡 **Active Slot {edit_slot} Schedule Target Blueprint Export Summary:**")
            st.code(f"📅 Target Post Date: {schedule_date}\n📝 Final Caption Text String Output:\n{caption_text}", language="text")
