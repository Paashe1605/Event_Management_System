import streamlit as st
import os
from db import get_connection, get_cursor, close_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

if "role" not in st.session_state or st.session_state["role"] != "user":
    st.warning("Access denied. Please log in as a User.")
    st.stop()

st.markdown("<h1 style='text-align: center;'>🎫 My Event Passes</h1>", unsafe_allow_html=True)

password_input = st.text_input("🔑 Please re-enter your login password", type="password")
submitted = st.button("Show My Passes")

if submitted and password_input:
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        # ✅ Get user info first
        cursor.execute("SELECT user_id, name, email, aadhar_number, password FROM users WHERE email=?", 
                       (st.session_state.get("email"),))
        user = cursor.fetchone()

        if not user:
            st.error("User not found.")
            close_connection(conn)
        else:
            user_id, name, email, aadhar, stored_password = user

            if password_input != stored_password:
                st.error("❌ Incorrect password. Please try again.")
                close_connection(conn)
            else:
                # ✅ Fetch all registrations for this user
                cursor.execute("""
                    SELECT r.pass_id, e.name, e.date, e.time, e.venue, e.logo_path,
                           e.final_entry_time, e.end_time, e.end_date
                    FROM registrations r
                    JOIN events e ON r.event_id = e.id
                    WHERE r.user_id = ?
                """, (user_id,))
                passes = cursor.fetchall()
                close_connection(conn)

                if not passes:
                    st.warning("No passes found for this user.")
                else:
                    st.success(f"Found {len(passes)} pass(es) for **{name}**!")
                    st.markdown("---")

                    for pass_data in passes:
                        pass_id, event, date, time, venue, logo_path, final_entry, end_time, end_date = pass_data

                        col_logo, col_title = st.columns([1, 3])
                        with col_logo:
                            if logo_path and os.path.exists(logo_path):
                                st.image(logo_path, width=80)
                        with col_title:
                            st.markdown(f"<h3 style='margin-top: 20px;'>{event} Pass</h3>", unsafe_allow_html=True)

                        st.write(f"**Name:** {name}")
                        st.write(f"**Pass ID:** {pass_id}")
                        st.write(f"**Date:** {date}")
                        st.write(f"**Time:** {time}")
                        st.write(f"**Final Entry Time:** {final_entry}")
                        st.write(f"**End Time:** {end_time}")
                        st.write(f"**End Date:** {end_date}")
                        st.write(f"**Venue:** {venue}")

                        photo_path = f"assets/photos/{aadhar}.jpg"
                        qr_path = f"assets/qrcodes/{pass_id}.png"
                        col1, col2 = st.columns([2, 2])
                        with col1:
                            if os.path.exists(photo_path):
                                st.image(photo_path, caption="User Photo", width=150)
                        with col2:
                            if os.path.exists(qr_path):
                                st.image(qr_path, caption="Your QR Code", width=150)

                        # ✅ Generate PDF for each pass
                        os.makedirs("assets/passes", exist_ok=True)
                        pdf_path = f"assets/passes/{pass_id}.pdf"
                        half_page = (A4[0], A4[1] / 2)
                        c = canvas.Canvas(pdf_path, pagesize=half_page)
                        c.setStrokeColor(colors.black)
                        c.setLineWidth(3)
                        c.rect(30, 30, half_page[0] - 60, half_page[1] - 60)

                        logo_x = 50
                        logo_y = half_page[1] - 100
                        if logo_path and os.path.exists(logo_path):
                            c.drawImage(logo_path, logo_x, logo_y, width=60, height=60)
                        c.setFont("Helvetica-Bold", 20)
                        c.drawString(logo_x + 80, logo_y + 20, f"{event} Pass")

                        c.setFont("Helvetica", 12)
                        c.drawString(50, logo_y - 30, f"Name: {name}")
                        c.drawString(50, logo_y - 50, f"Pass ID: {pass_id}")
                        c.drawString(50, logo_y - 70, f"Date: {date}")
                        c.drawString(50, logo_y - 90, f"Time: {time}")
                        c.drawString(50, logo_y - 110, f"Final Entry: {final_entry}")
                        c.drawString(50, logo_y - 130, f"End Time: {end_time}")
                        c.drawString(50, logo_y - 150, f"End Date: {end_date}")
                        c.drawString(50, logo_y - 170, f"Venue: {venue}")

                        if os.path.exists(photo_path):
                            c.drawImage(photo_path, 50, 40, width=100, height=100)
                        if os.path.exists(qr_path):
                            c.drawImage(qr_path, half_page[0] - 180, 40, width=120, height=120)

                        c.save()
                        with open(pdf_path, "rb") as f:
                            st.download_button(f"📄 Download {event} Pass (PDF)", f, file_name=os.path.basename(pdf_path))

                        st.markdown("---")

    except Exception as e:
        st.error(f"An error occurred: {e}")