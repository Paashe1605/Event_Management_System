# app.py the main file fr the Project.
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Event Management System", page_icon="C:\\Users\\paara\\Downloads\\Designer (2).png", layout="centered")
st.session_state.setdefault("navigate_to", None)

# ---- Sequential Animations ----
st.markdown("""
<style>
/* Headings appear first */
h1 {
  animation: slideInLeft 1s ease-out both;
}
h2 {
  animation: slideInRight 1.2s ease-out both;
}

/* Paragraphs fade in after headings */
p {
  animation: fadeInText 1.4s ease-out both;
}

/* Lists stagger upward one by one */
ul li {
  animation: slideUpList 1s ease-out both;
}
ul li:nth-child(1) { animation-delay: 1.6s; }
ul li:nth-child(2) { animation-delay: 1.8s; }
ul li:nth-child(3) { animation-delay: 2s; }
ul li:nth-child(4) { animation-delay: 2.2s; }
ul li:nth-child(5) { animation-delay: 2.4s; }

/* Images pulse in after text */
img {
  animation: pulseImage 2.6s ease-in-out both;
  transition: transform 300ms ease, box-shadow 300ms ease, filter 300ms ease;
  border-radius: 12px;
}
img:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 28px rgba(0,0,0,0.15);
  filter: brightness(1.05);
}

/* Alerts bounce in later */
.stAlert {
  animation: bounceIn 2.8s ease-out both;
}

/* Captions slide subtly at the end */
.caption {
  animation: slideOutText 3s ease-in-out infinite alternate;
}

/* Keyframes */
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-50px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(50px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInText {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUpList {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseImage {
  0% { transform: scale(0.97); opacity: 0.8; }
  50% { transform: scale(1.02); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes bounceIn {
  0% { transform: scale(0.9); opacity: 0; }
  60% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); }
}
@keyframes slideOutText {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(20px); opacity: 0.8; }
}
</style>
""", unsafe_allow_html=True)

# ---- Original content (unchanged) ----
st.markdown(
    "<h1 style='text-align:center; margin-bottom: 0.25rem;'>🌟Event Management System 📊</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h2 style='text-align:center; color: #6c757d; margin-top: 0;'> Event Management & Pass Distribution Made Digital And Simple </h2>",
    unsafe_allow_html=True,
)
st.markdown("---")

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

st.info("⚙️ Quick Guide to get started:🧭⏬")
st.info("👉 From the left menu, click **Login** to sign in as User/Admin")
st.info("👉 As **Admin**: Visit **Admin Dashboard** to add events, generate passes, and export CSVs")
st.info("👉 As **User**: Register as new user and generate digital pass PDFs or login with your credentials to view passes.")

st.markdown("---")

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

if "role" in st.session_state and st.session_state.get("role"):
    display_email = st.session_state.get("email", "unknown")
    st.caption(f"Signed in as {st.session_state['role'].title()} — {display_email}")
else:
    st.caption(" This Prototype/Project Built as a proof-of-concept by Paaras Shemrudkar @ Exigotech TSP.")