# app.py
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Event Management System", page_icon="C:\\Users\\paara\\Downloads\\Designer (2).png", layout="centered")

# Do NOT set st.session_state["role"] here — leave login.py free to create it when needed.
# Keep a navigation placeholder only if you need it later (optional)
st.session_state.setdefault("navigate_to", None)

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

# Two-column hero with brief and highlights
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

st.markdown("---")
 # Feature cards (three columns)
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

   
with col2:
    st.image(
        "C:\\Users\\paara\\Downloads\\Designer (1).png",
        width=500,
    )
    st.markdown("<div style='text-align:center; margin-top: 0.5rem;'>"
                "<strong style='font-size:1rem;'>Fast demo flow</strong><br>"
                "Prepare: add an event → register a user → generate pass"
                "</div>", unsafe_allow_html=True)

st.markdown("---")
st.info("⚙️             Quick Guide to get started:🧭⏬")
st.info("👉 From the left menu, click **Login** to sign in as User/Admin")
st.info("👉 As **Admin**:Visit **Admin Dashboard** to add events, generate passes, and export CSVs")
st.info("👉 As **User**:Register as new user and generate digital pass PDFs or login with your credentials , to view you passes.")

st.markdown("---")

# Quick-start checklist
st.markdown("### Quick-start checklist for demos")
st.markdown(dedent("""
- Ensure the app is running: `python -m streamlit run app.py`  
- Open the left menu and click **Login** to sign in as User/Admin 
- As **User**:  
  - Visit **Register User** to create a user  
  - Visit **Generate Pass** to create and download a digital pass PDF 
- Visit **Admin Dashboard** to add events, generate passes, and export CSVs  
- Audit log file: `assets/audit/export_log.csv` (exports are logged automatically)
"""))

st.markdown("---")

# Footer note
# Safely show sign-in status only if the "role" key exists and is not None
if "role" in st.session_state and st.session_state.get("role"):
    display_email = st.session_state.get("email", "unknown")
    st.caption(f"Signed in as {st.session_state['role'].title()} — {display_email}")
else:
    st.caption(" This Prototype/Project Built as a proof-of-concept by Paaras Shemrudkar @ Exigotech TSP.")