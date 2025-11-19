import streamlit as st
from db import get_connection, get_cursor, close_connection

# ---- Animations & UI polish (no logic/theme changes) ----
st.markdown("""
<style>
/* Heading slide-in */
h2 {
  animation: slideInDown 1.2s ease-out both;
}

/* Inputs fade-in */
input, select {
  animation: fadeInField 1s ease-out both;
}

/* Alerts bounce-in */
.stAlert {
  animation: bounceIn 1s ease-out both;
}

/* Buttons pulse on hover */
button[kind="primary"], button[kind="secondary"] {
  transition: transform 250ms ease, box-shadow 250ms ease;
}
button[kind="primary"]:hover, button[kind="secondary"]:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

/* Keyframes */
@keyframes slideInDown {
  from { opacity: 0; transform: translateY(-40px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInField {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes bounceIn {
  0% { transform: scale(0.9); opacity: 0; }
  60% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

def login():
    st.markdown("<h2 style='text-align:center;'>🔐 Login Portal</h2>", unsafe_allow_html=True)
    role = st.selectbox("Select Role", ["User", "Admin"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT password FROM users WHERE email = ? AND LOWER(role) = ?", (email, role.lower()))
        result = cursor.fetchone()

        close_connection(conn)

        if result and result[0] == password:
            st.success(f"Welcome, {role.title()}!")
            st.session_state["role"] = role.lower()
            st.session_state["email"] = email
            st.session_state["from_login"] = True

            if role.lower() == "admin":
                st.switch_page("pages/admin_dashboard.py")
            else:
                st.switch_page("pages/my_pass.py")
        else:
            st.error("Invalid credentials or role mismatch.")

# 🔁 Registration redirect
if st.button("New user? Register here"):
    st.session_state["from_login"] = True
    st.switch_page("pages/register.py")

# 🔐 Run login logic
if "role" not in st.session_state:
    login()
else:
    st.info(f"Logged in as: {st.session_state['role'].title()} ({st.session_state['email']})")    

# --- Logout button ---
if st.button("🚪 Logout"):
    # Clear session state keys
    for key in ["role", "email", "from_login", "navigate_to"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("You have been logged out.")
    st.rerun()