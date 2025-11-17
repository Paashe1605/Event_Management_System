import streamlit as st

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