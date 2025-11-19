# app.py the main file fr the Project.
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Event Management System", page_icon="C:\\Users\\paara\\Downloads\\Designer (2).png", layout="centered")
st.session_state.setdefault("navigate_to", None)

# ---- Text Animations (slide-in, slide-out, bounce, fade) ----
st.markdown("""
<style>
/* Fade-in for all text blocks */
[data-testid="stMarkdownContainer"] p, h1, h2, h3, h4, h5, h6 {
  animation: fadeInText 1s ease-out both;
}

/* Slide-in for headings */
h1, h2 {
  animation: slideInText 1.2s ease-out both;
}

/* Bounce for feature titles */
h3 {
  animation: bounceText 1.5s ease-in-out both;
}

/* Slide-out subtle loop for captions */
.caption {
  animation: slideOutText 4s ease-in-out infinite alternate;
}

/* Keyframes */
@keyframes fadeInText {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideInText {
  from { opacity: 0; transform: translateX(-40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes bounceText {
  0% { transform: translateY(0); }
  30% { transform: translateY(-8px); }
  60% { transform: translateY(4px); }
  100% { transform: translateY(0); }
}
@keyframes slideOutText {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(20px); opacity: 0.8; }
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    "<h1 style='text-align:center; margin-bottom: 0.25rem;'>🌟Event Management System 📊</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h2 style='text-align:center; color: #6c757d; margin-top: 0;'> Event Management & Pass Distribution Made Digital And Simple </h2>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Two-column hero
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(dedent("""
        **Welcome!**  

        This project/prototype/proof-of-concept streamlines Event Management by replacing paper passes with secure
        digital passes and an easy-to-use admin interface to manage events.

        Key capabilities:
                        
        - Generate and manage event passes as professional PDFs 📄
        - Create, edit, open/close, and delete events quickly ⚙️
        - Register users and issue passes (Admin flows protected) 🔐
        - Export Users and Passes to CSV with Aadhaar masking and audit logging 🔒
        - Built using Defensive Database Queries to avoid runtime errors ✅
    """))

with col2:
    st.image("C:\\Users\\paara\\Downloads\\Designer (1).png", width=500)
    st.image("C:\\Users\\paara\\Downloads\\Designer (5).png", width=300)

st.markdown("---")

# Feature cards
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 🗂️ Events")
    st.write("Create and manage events with capacity, timings, and logo support.")
with c2:
    st.markdown("### 👥 Users")
    st.write("Register attendees, mask Aadhaar in exports, and keep audit trails.")
with c3:
    st.markdown("### 🎟️ Passes")
    st.write("Generate, preview, and verify digital passes; PDFs stored under assets/passes.")

st.markdown("---")

# Quick Guide
st.info("⚙️ Quick Guide to get started:🧭⏬")
st.info("👉 From the left menu, click **Login** to sign in as User/Admin")
st.info("👉 As **Admin**: Visit **Admin Dashboard** to add events, generate passes, and export CSVs")
st.info("👉 As **User**: Register as new user and generate digital pass PDFs or login with your credentials to view passes.")

st.markdown("---")

# Quick-start checklist
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Quick-start checklist for demos")
    st.markdown(dedent("""
    - Ensure the app is running: `python -m streamlit run app.py`  
    - Open the left menu and click **Login** to sign in as User/Admin 
    - As **User**:  
        - Visit **Register User** to create a user  
        - Visit **Generate Pass** to create and download a digital pass PDF 
    - Visit **Admin Dashboard** to add events, generate passes, and export CSVs  
    - Explore the codebase to understand implementation details
    """))
with col2:
    st.image("C:\\Users\\paara\\Downloads\\Designer (3).png", width=300)

st.markdown("---")

# Footer
if "role" in st.session_state and st.session_state.get("role"):
    display_email = st.session_state.get("email", "unknown")
    st.caption(f"Signed in as {st.session_state['role'].title()} — {display_email}")
else:
    st.caption(" This Prototype/Project Built as a proof-of-concept by Paaras Shemrudkar @ Exigotech TSP.")