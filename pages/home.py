import streamlit as st

# ---- Animations & UI polish  ----
st.markdown("""
<style>
/* Headings slide-in */
h2 {
  animation: slideIn 1.2s ease-out both;
}

/* Paragraphs fade-in */
p {
  animation: fadeInText 1s ease-out both;
}

/* Lists staggered slide-up */
ul li {
  animation: slideUpList 1s ease-out both;
}
ul li:nth-child(2) { animation-delay: 0.2s; }
ul li:nth-child(3) { animation-delay: 0.4s; }
ul li:nth-child(4) { animation-delay: 0.6s; }

/* Alerts bounce-in */
.stAlert {
  animation: bounceIn 1s ease-out both;
}

/* Logout button hover pulse */
button[kind="primary"] {
  transition: transform 250ms ease, box-shadow 250ms ease;
}
button[kind="primary"]:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

/* Keyframes */
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-40px); }
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
@keyframes bounceIn {
  0% { transform: scale(0.9); opacity: 0; }
  60% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# Guard: only proceed if role exists and is not None
if "role" not in st.session_state or not st.session_state.get("role"):
    st.warning("⚠️ You are Currently Logged out, Please log in first.")
    st.stop()

role = st.session_state["role"].lower()

# --- User view ---
if role == "user":
    st.markdown("<h2 style='text-align:center;'>🎉 Welcome User!</h2>", unsafe_allow_html=True)
    st.markdown("""
    **Here’s your flow in the app:**
    - 📝 Register yourself for events 
    - 🎭 Browse and select cultural events  
    - 💳 Complete payments securely
    - 🎟️ View and download your digital pass anytime by logging in. 
    """)
    st.info("Tip: Your pass is always available under **My Pass** in the sidebar.")

# --- Admin view ---
elif role == "admin":
    st.markdown("<h2 style='text-align:center;'>🛠️ Welcome Admin!</h2>", unsafe_allow_html=True)
    st.markdown("""
    **Here’s your flow in the app:**
    - ➕ Create new events with capacity and timings
    - 🗂️ Manage existing events (edit, open/close, delete)
    - 👥 Register users and issue passes through the admin dashboard
    - 📊 Export users/passes to CSV with Aadhaar masking
    - 🔍 Verify passes and maintain audit logs  
    """)
    st.info("Tip: Use the **Admin Dashboard** in the sidebar for full controls.")

else:
    st.warning("Unknown role. Please log in again.")
    st.stop()

# --- Logout button ---
if st.button("🚪 Logout"):
    # Clear session state keys
    for key in ["role", "email", "from_login", "navigate_to"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("You have been logged out.")
    st.rerun()