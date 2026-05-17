import streamlit as st
from PIL import Image

# 🎨 Page Configuration & Title Styling
st.set_page_config(
    page_title="InstaGrid Previewer | Dilshad Pro",
    page_icon="📸",
    layout="centered"
)

# 🔒 Clean Custom CSS Variable (Safely isolated to prevent line parsing TypeErrors)
custom_css = """
<style>
.main {
    background: radial-gradient(circle at top, #1e1b4b, #0f172a, #020617) !important;
}
div[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #1e1b4b, #0f172a, #020617) !important;
}
h1, h2, h3, p, span, label {
    color: #f8fafc !important;
    font-family: '-apple-system', BlinkMacSystemFont, sans-serif !important;
}
.phone-mock {
    background: rgba(23, 32, 48, 0.7);
    padding: 24px;
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    margin-bottom: 25px;
}
</style>
"""

# 🎯 FIXED: Changed 'unsafe_with_html' to 'unsafe_allow_html'
st.markdown(custom_css, unsafe_allow_html=True)

st.title("📸 InstaGrid Layout Previewer")
st.caption("Engineered by Dilshad • Powered by Streamlit")

# Initialize session state tracking list for images if not already created
if "image_list" not in st.session_state:
    st.session_state.image_list = []

# --- SIDEBAR INTERFACE CONTROLS ---
st.sidebar.header("⚙️ Grid Control Panel")

# Multi-file Uploader Widget
uploaded_files = st.sidebar.file_uploader(
    "Upload Feed Photos (Max 12)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

# Process uploaded images dynamically into session storage state
if uploaded_files:
    new_images = []
    for file in uploaded_files:
        img = Image.open(file)
        new_images.append(img)
    st.session_state.image_list = new_images

# Button to reset grid canvas parameters
if st.sidebar.button("🗑️ Clear Current Grid"):
    st.session_state.image_list = []
    st.rerun()

# --- MAIN COMPONENT PHONE DISPLAY VIEWPORT ---
st.markdown('<div class="phone-mock">', unsafe_allow_html=True)

# Mock Instagram Profile Header Segment
col_av, col_txt = st.columns([1, 4])
with col_av:
    st.subheader("👤") 
with col_txt:
    st.markdown("### **@your_brand_feed**")
    st.markdown(f"**{len(st.session_state.image_list)}** posts &nbsp;&nbsp;•&nbsp;&nbsp; **12.5K** followers &nbsp;&nbsp;•&nbsp;&nbsp; **482** following")
    st.caption("Grid Layout Planner. Arrange your images in the sidebar to view the final grid mapping!")

st.markdown("---")

# 🖼️ THE ESSENTIAL 3-COLUMN IMAGE STREAM GRID MATRIX
if st.session_state.image_list:
    total_pics = len(st.session_state.image_list)
    
    # Calculate rows to cleanly display items in blocks of 3
    for i in range(0, total_pics, 3):
        row_images = st.session_state.image_list[i:i+3]
        cols = st.columns(3) # Forces an exact rigid 3-column split
        
        for idx, img in enumerate(row_images):
            with cols[idx]:
                st.image(img, use_container_width=True)
else:
    st.info("💡 Open the left sidebar panel menu to upload images and generate your visual feed preview model instantly!")

st.markdown('</div>', unsafe_allow_html=True)

# --- REORDERING UTILITY TOOL BLOCK CONTROLLER SYSTEM ---
if len(st.session_state.image_list) > 1:
    st.markdown("### 🔄 Adjust Position Index Order")
    st.caption("Move your uploaded images around by changing their sequential positions:")
    
    img_index = st.number_input("Select Image Index to move", min_value=0, max_value=len(st.session_state.image_list)-1, step=1, value=0)
    new_position = st.slider("Move selected item to target position", min_value=0, max_value=len(st.session_state.image_list)-1, value=int(img_index))
    
    if st.button("Confirm Order Swap"):
        moving_item = st.session_state.image_list.pop(img_index)
        st.session_state.image_list.insert(new_position, moving_item)
        st.success("Grid order updated successfully!")
        st.rerun()
