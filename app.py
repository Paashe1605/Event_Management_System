# app.py the main file fr the Project.
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Event Management System", page_icon="✨", layout="centered")
st.session_state.setdefault("navigate_to", None)

# ---- Sequential Animation using CSS Keyframes ----
st.markdown("""
<style>
/* 
   ================================================================
   ANIMATIONS FOR STREAMLIT EVENT MANAGEMENT SYSTEM
   ================================================================
*/

/* 1. Headings: Elastic Bouncing Entrances */
h1 {
  animation: elasticDrop 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) both !important;
}

h2 {
  animation: slideInBlur 1.5s ease-out both !important;
  animation-delay: 0.3s;
}

h3 {
  animation: popIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) both !important;
}

/* 2. General Text: Slide Up Fade */
p {
  animation: fadeInUp 1.2s ease-out both;
}

/* 3. Lists: Aggressive Staggered Snap-In */
ul li {
  opacity: 0; /* Start hidden */
  animation: slideInRightSnap 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  transform-origin: left center;
}

/* Stagger delays to make it flow like a waterfall */
ul li:nth-child(1) { animation-delay: 1.0s; }
ul li:nth-child(2) { animation-delay: 1.1s; }
ul li:nth-child(3) { animation-delay: 1.2s; }
ul li:nth-child(4) { animation-delay: 1.3s; }
ul li:nth-child(5) { animation-delay: 1.4s; }

/* Hover effect for list items (Interactive) */
ul li:hover {
  transform: translateX(15px) scale(1.02);
  transition: transform 0.2s ease-out;
}

/* 4. Images: Continuous Floating & Breathing */
img {
  /* Enters with zoom, then floats forever */
  animation: zoomEntrance 1s ease-out both, floatBob 6s ease-in-out infinite 1s !important;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1); /* Subtle shadow to add depth */
}

img:hover {
  transform: scale(1.1) rotate(3deg) !important;
  z-index: 10;
}

/* 5. Alerts: Gelatin Wiggle Effect */
.stAlert {
  animation: gelatin 1s both;
  transform-origin: center;
}
/* Delay alerts so they pop in late */
.stAlert:nth-of-type(1) { animation-delay: 2.0s; }
.stAlert:nth-of-type(2) { animation-delay: 2.2s; }
.stAlert:nth-of-type(3) { animation-delay: 2.4s; }

/* 6. Horizontal Rules: Expand outward */
hr {
  animation: expandLine 1.5s ease-in-out forwards;
  transform-origin: center;
  width: 0%;
}

/* 7. Buttons/Interactives (if any): subtle pulse */
button {
  animation: pulse 2s infinite;
}

/* ================= KEYFRAMES ================= */

@keyframes elasticDrop {
  0% { transform: translateY(-100px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

@keyframes slideInBlur {
  0% { filter: blur(10px); opacity: 0; transform: translateX(-50px); }
  100% { filter: blur(0); opacity: 1; transform: translateX(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translate3d(0, 40px, 0); }
  to { opacity: 1; transform: translate3d(0, 0, 0); }
}

@keyframes slideInRightSnap {
  0% { opacity: 0; transform: translateX(-30px); }
  100% { opacity: 1; transform: translateX(0); }
}

@keyframes zoomEntrance {
  0% { opacity: 0; transform: scale(0.5); }
  100% { opacity: 1; transform: scale(1); }
}

/* The "Alive" floating effect */
@keyframes floatBob {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
  100% { transform: translateY(0px); }
}

/* Wobbly pop-in effect */
@keyframes gelatin {
  0% { transform: scale(1, 1); opacity: 0; }
  25% { transform: scale(0.9, 1.1); }
  50% { transform: scale(1.1, 0.9); opacity: 1; }
  75% { transform: scale(0.95, 1.05); }
  100% { transform: scale(1, 1); opacity: 1; }
}

@keyframes popIn {
  0% { transform: scale(0); opacity: 0; }
  80% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes expandLine {
  0% { width: 0%; opacity: 0; }
  100% { width: 100%; opacity: 1; }
}

</style>
""", unsafe_allow_html=True)

# ---- Original content  ----
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
    st.markdown(
        f"""
        <div style="font-size:17px;">
        {dedent("""\
                
        **Welcome!**  

        This project/prototype/proof-of-concept streamlines Event Management by replacing paper passes with secure
        digital passes and an easy-to-use admin interface to manage events.
        
        ---
        Key capabilities:
                        
        - Generate and manage event passes as professional PDFs 📄
        - Create, edit, open/close, and delete events quickly ⚙️
        - Register users and issue passes (Admin flows protected) 🔐
        - Export Users and Passes to CSV with Aadhaar masking and audit logging 🔒
        - Built using Defensive Database Queries to avoid runtime errors ✅
        """)}</div>
        
        """,
        unsafe_allow_html=True
    )
with col2:
    st.image("D:\\event_management_system\\assets\\Designer (1).png", width=300)
    st.image("D:\\event_management_system\\assets\\Designer (5).png", width=300)

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
    st.image("D:\\event_management_system\\assets\\Designer (3).png", width=300)

st.markdown("---")

if "role" in st.session_state and st.session_state.get("role"):
    display_email = st.session_state.get("email", "unknown")
    st.caption(f"Signed in as {st.session_state['role'].title()} — {display_email}")
else:
    st.caption(" This Prototype/Project Built as a proof-of-concept by Paaras Shemrudkar @ INTERNSHIP..")