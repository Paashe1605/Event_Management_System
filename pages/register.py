import streamlit as st
import sqlite3
import os
import uuid
import qrcode
import time   # <-- added for progress bar animation
from db import get_connection, get_cursor, close_connection

# 🔐 Access control
if "from_login" not in st.session_state or not st.session_state["from_login"]:
    st.warning("Access denied. Please use the login page to register.")
    st.stop()

# 📝 Registration form with animation
st.markdown(
    """
    <style>
    /* Fade-in animation for the form */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .animated-form {
        animation: fadeIn 1s ease-in-out;
    }

    /* Button hover effect */
    div.stButton > button:first-child {
        transition: all 0.3s ease;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        background-color: #45a049;
    }

    /* Success message pulse */
    .success-anim {
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.02);}
        100% {transform: scale(1);}
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 style='text-align:center;'>📝 User Registration</h2>", unsafe_allow_html=True)
st.write("Please fill in your details to register for any ongoing events.")

# --- Load only open events ---
try:
    conn = get_connection()
    cursor = get_cursor(conn)
    cursor.execute("SELECT id, name, capacity FROM events WHERE status='open'")
    open_events = cursor.fetchall()
    close_connection(conn)
except Exception as e:
    st.error(f"Error loading events: {e}")
    open_events = []

event_names = [ev[1] for ev in open_events] if open_events else []

with st.form("user_registration_form"):
    st.markdown('<div class="animated-form">', unsafe_allow_html=True)

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    password = st.text_input("Create Password", type="password")
    event = st.selectbox("Select Event", event_names if event_names else ["No open events available"])
    aadhar = st.text_input("Aadhar Number")
    photo = st.file_uploader("Upload Your Photo", type=["jpg", "jpeg", "png"])

    # Mock Payment Section
    st.subheader("💳 Payment Details (Mock)")
    upi_id = st.text_input("Enter UPI ID")
    upi_pin = st.text_input("Enter 4-digit UPI PIN (mock)", type="password")
    payment_confirmed = st.checkbox("I confirm payment of ₹100 for the selected event")

    submitted = st.form_submit_button("Register")

    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    # --- Animated progress bar ---
    progress_text = "⏳ Processing your registration..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(0, 101, 10):
        time.sleep(0.1)  # smooth animation
        my_bar.progress(percent_complete, text=progress_text)

    if not all([name, age, gender, address, phone, email, password, aadhar, event]):
        st.error("Please fill in all fields.")
    elif not payment_confirmed or not upi_id or not upi_pin:
        st.warning("Please complete payment details to proceed.")
    elif event == "No open events available":
        st.error("No events are currently open for registration.")
    else:
        try:
            # Save photo if uploaded
            if photo:
                os.makedirs("assets/photos", exist_ok=True)
                photo_path = f"assets/photos/{aadhar}.jpg"
                with open(photo_path, "wb") as f:
                    f.write(photo.getbuffer())
            else:
                st.warning("No photo uploaded. You can upload it later.")

            # Check capacity
            conn = get_connection()
            cursor = get_cursor(conn)

            cursor.execute("SELECT id, capacity FROM events WHERE name=? AND status='open'", (event,))
            ev = cursor.fetchone()
            if not ev:
                st.error("Selected event is not open anymore.")
                close_connection(conn)
            else:
                event_id, capacity = ev
                cursor.execute("SELECT COUNT(*) FROM registrations WHERE event_id=?", (event_id,))
                current_count = cursor.fetchone()[0]

                if current_count >= capacity:
                    st.error("This event has reached maximum capacity. Registration closed.")
                    close_connection(conn)
                else:
                    # Check if user already exists
                    cursor.execute("SELECT user_id FROM users WHERE email=?", (email,))
                    user = cursor.fetchone()

                    if user:
                        user_id = user[0]
                    else:
                        # New user → insert into users
                        cursor.execute("""
                            INSERT INTO users (name, age, gender, address, phone, email, password, aadhar_number, role)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (name, age, gender, address, phone, email, password, aadhar, "user"))
                        user_id = cursor.lastrowid  # now matches user_id PK

                    # Generate unique pass Id
                    pass_id = str(uuid.uuid4())[:8]

                    # Insert into registrations
                    cursor.execute("""
                        INSERT INTO registrations (user_id, event_id, pass_id)
                        VALUES (?, ?, ?)
                    """, (user_id, event_id, pass_id))

                    # Generate QR code
                    qr_data = f"PassID:{pass_id}|Name:{name}|Email:{email}|Aadhar:{aadhar}|Event:{event}"
                    qr_img = qrcode.make(qr_data)

                    os.makedirs("assets/qrcodes", exist_ok=True)
                    qr_path = f"assets/qrcodes/{pass_id}.png"
                    qr_img.save(qr_path)

                    conn.commit()
                    close_connection(conn)

                    st.success(f"🎉 Payment Successful & Registration successful for {event}!")
                    st.markdown('<p class="success-anim">✅ Your digital pass has been generated automatically. You can view it in your My Passes section.</p>', unsafe_allow_html=True)
                    st.balloons()
                    st.session_state["from_login"] = False

        except Exception as e:
            st.error(f"An error occurred: {e}")