import streamlit as st
import os
import csv
from io import StringIO
from datetime import datetime
from db import get_connection, get_cursor, close_connection

# 🔐 Access control
if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.warning("Access denied. Please log in as an Admin.")
    st.stop()

# Sidebar navigation
st.sidebar.title("🛠️ Admin Dashboard")
page = st.sidebar.radio("Navigate", ["Events", "Users", "Passes", "Generate Pass", "Verify Pass"])

# Helpers
def _safe_filename_part(s: str):
    return "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in s).strip()

def _mask_aadhaar(aadhaar: str) -> str:
    if not aadhaar:
        return ""
    s = "".join(ch for ch in aadhaar if ch.isdigit())
    if len(s) <= 4:
        return s
    return "X" * (len(s) - 4) + s[-4:]

def _to_csv_string(rows, headers):
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    writer.writerows(rows)
    return buf.getvalue()

def _download_button_bytes(label: str, data: bytes, file_name: str, mime: str = "text/csv"):
    return st.download_button(label=label, data=data, file_name=file_name, mime=mime)

def _has_column(table: str, column: str) -> bool:
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(f"PRAGMA table_info({table})")
        cols = [r[1] for r in cursor.fetchall()]
        close_connection(conn)
        return column in cols
    except Exception:
        return False

# Audit logging
AUDIT_DIR = os.path.join("assets", "audit")
os.makedirs(AUDIT_DIR, exist_ok=True)
AUDIT_LOG = os.path.join(AUDIT_DIR, "export_log.csv")
if not os.path.exists(AUDIT_LOG):
    with open(AUDIT_LOG, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_utc", "admin_user", "export_type", "row_count", "file_name"])

def _log_export(admin_user: str, export_type: str, row_count: int, file_name: str):
    ts = datetime.utcnow().isoformat()
    with open(AUDIT_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([ts, admin_user, export_type, row_count, file_name])

LOGO_DIR = os.path.join("assets", "logos")
os.makedirs(LOGO_DIR, exist_ok=True)
PASS_PDF_DIR = os.path.join("assets", "passes")
os.makedirs(PASS_PDF_DIR, exist_ok=True)

# --- EVENTS PAGE ---
if page == "Events":
    st.header("📅 Event Management")
    st.info("Create, edit, open/close, and delete events.")

    with st.form("add_event"):
        event_name = st.text_input("Event Name", key="add_name")
        event_date = st.date_input("Event Date", key="add_date")
        event_time = st.text_input("Start Time (HH:MM)", placeholder="e.g., 18:30", key="add_time")
        final_entry_time = st.text_input("Final Entry Time (HH:MM)", placeholder="e.g., 19:00", key="add_final")
        end_time = st.text_input("End Time (HH:MM)", placeholder="e.g., 21:00", key="add_end_time")
        end_date = st.date_input("End Date", key="add_end_date")
        venue = st.text_input("Venue", key="add_venue")
        capacity = st.number_input("Capacity", min_value=1, step=1, key="add_capacity")
        logo_file = st.file_uploader("Upload Event Logo (optional)", type=["jpg", "png", "jpeg"], key="add_logo")
        submitted = st.form_submit_button("Add Event")

        if submitted:
            if not event_name or not event_time or not final_entry_time or not end_time or not venue:
                st.error("Please fill all required fields.")
            else:
                try:
                    conn = get_connection()
                    cursor = get_cursor(conn)
                    cursor.execute("SELECT COUNT(*) FROM events WHERE name=? AND date=?", (event_name.strip(), str(event_date)))
                    if cursor.fetchone()[0] > 0:
                        close_connection(conn)
                        st.error("An event with the same name and date already exists.")
                    else:
                        logo_path = None
                        if logo_file:
                            ext = os.path.splitext(logo_file.name)[1].lower()
                            safe_name = f"{_safe_filename_part(event_name)}_{event_date}{ext}"
                            logo_path = os.path.join(LOGO_DIR, safe_name)
                            with open(logo_path, "wb") as f:
                                f.write(logo_file.read())

                        cursor.execute("""
                            INSERT INTO events (name, date, time, venue, capacity, logo_path, status,
                                                final_entry_time, end_time, end_date)
                            VALUES (?, ?, ?, ?, ?, ?, 'open', ?, ?, ?)
                        """, (
                            event_name.strip(),
                            str(event_date),
                            event_time.strip(),
                            venue.strip(),
                            int(capacity),
                            logo_path,
                            final_entry_time.strip(),
                            end_time.strip(),
                            str(end_date)
                        ))
                        conn.commit()
                        close_connection(conn)
                        st.session_state["event_added"] = event_name.strip()
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to add event: {e}")

    if "event_added" in st.session_state:
        st.success(f"Event '{st.session_state['event_added']}' added successfully.")
        del st.session_state["event_added"]
    if "event_closed" in st.session_state:
        st.success(f"{st.session_state['event_closed']} closed.")
        del st.session_state["event_closed"]
    if "event_opened" in st.session_state:
        st.success(f"{st.session_state['event_opened']} opened.")
        del st.session_state["event_opened"]
    if "event_deleted" in st.session_state:
        st.warning(f"{st.session_state['event_deleted']} deleted.")
        del st.session_state["event_deleted"]
    if "event_updated" in st.session_state:
        st.success(f"{st.session_state['event_updated']} updated.")
        del st.session_state["event_updated"]

    st.subheader("All Events")
    col_f1, col_f2, col_f3 = st.columns([3, 1, 2])
    with col_f1:
        q = st.text_input("Search by name or venue", key="filter_q")
    with col_f2:
        status_filter = st.selectbox("Status", ["All", "open", "closed"], key="filter_status")
    with col_f3:
        date_filter = st.date_input("On date (Please also select date of event to sort & search.)", key="filter_date")

    query = "SELECT id, name, date, time, venue, capacity, status, logo_path, final_entry_time, end_time, end_date FROM events WHERE 1=1"
    params = []
    if q:
        query += " AND (name LIKE ? OR venue LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if status_filter and status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    try:
        if "filter_date" in st.session_state and st.session_state["filter_date"] is not None:
            if date_filter:
                query += " AND date = ?"
                params.append(str(date_filter))
    except Exception:
        pass
    query += " ORDER BY date ASC, time ASC"

    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(query, tuple(params))
        events = cursor.fetchall()
        close_connection(conn)

        if events:
            for eid, name, date, time, venue, capacity, status, logo_path, final_entry_time, end_time, end_date in events:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
                with col1:
                    st.write(f"**{name}**")
                    st.caption(f"{date} • {time} • {venue}")
                    st.caption(f"Final entry: {final_entry_time} • Ends: {end_time} • End date: {end_date}")
                with col2:
                    st.write(f"Capacity: {capacity}")
                with col3:
                    st.write(f"Status: {status}")
                with col4:
                    if st.button("Close", key=f"close_{eid}"):
                        try:
                            conn = get_connection()
                            cursor = get_cursor(conn)
                            cursor.execute("UPDATE events SET status='closed' WHERE id=?", (eid,))
                            conn.commit()
                            close_connection(conn)
                            st.session_state["event_closed"] = name
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to close event: {e}")
                    if st.button("Open", key=f"open_{eid}"):
                        try:
                            conn = get_connection()
                            cursor = get_cursor(conn)
                            cursor.execute("UPDATE events SET status='open' WHERE id=?", (eid,))
                            conn.commit()
                            close_connection(conn)
                            st.session_state["event_opened"] = name
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to open event: {e}")
                    if st.button("Delete", key=f"delete_{eid}"):
                        try:
                            conn = get_connection()
                            cursor = get_cursor(conn)
                            cursor.execute("DELETE FROM events WHERE id=?", (eid,))
                            conn.commit()
                            close_connection(conn)
                            st.session_state["event_deleted"] = name
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete event: {e}")

                with st.expander("Edit event details", expanded=False):
                    form_key = f"edit_form_{eid}"
                    with st.form(form_key):
                        new_name = st.text_input("Event Name", value=name, key=f"name_{eid}")
                        try:
                            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                        except Exception:
                            parsed_date = None
                        new_date = st.date_input("Event Date", value=parsed_date, key=f"date_{eid}")
                        new_time = st.text_input("Start Time (HH:MM)", value=time or "", key=f"time_{eid}")
                        new_final = st.text_input("Final Entry Time (HH:MM)", value=final_entry_time or "", key=f"final_{eid}")
                        new_end_time = st.text_input("End Time (HH:MM)", value=end_time or "", key=f"end_time_{eid}")
                        try:
                            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        except Exception:
                            parsed_end_date = None
                        new_end_date = st.date_input("End Date", value=parsed_end_date, key=f"end_date_{eid}")
                        new_venue = st.text_input("Venue", value=venue or "", key=f"venue_{eid}")
                        new_capacity = st.number_input("Capacity", min_value=1, value=int(capacity), key=f"cap_{eid}")
                        replace_logo = st.file_uploader("Replace Event Logo (leave empty to keep)", type=["jpg", "png", "jpeg"], key=f"logo_{eid}")
                        save = st.form_submit_button("Save Changes")

                        if save:
                            if not new_name or not new_time or not new_final or not new_end_time or not new_venue:
                                st.error("Please fill all required fields.")
                            else:
                                try:
                                    conn = get_connection()
                                    cursor = get_cursor(conn)
                                    cursor.execute("SELECT COUNT(*) FROM events WHERE name=? AND date=? AND id!=?", (new_name.strip(), str(new_date), eid))
                                    if cursor.fetchone()[0] > 0:
                                        close_connection(conn)
                                        st.error("Another event with the same name and date already exists.")
                                    else:
                                        new_logo_path = logo_path
                                        if replace_logo:
                                            ext = os.path.splitext(replace_logo.name)[1].lower()
                                            safe_name = f"{_safe_filename_part(new_name)}_{new_date}{ext}"
                                            new_logo_path = os.path.join(LOGO_DIR, safe_name)
                                            with open(new_logo_path, "wb") as f:
                                                f.write(replace_logo.read())

                                        cursor.execute("""
                                            UPDATE events
                                            SET name=?, date=?, time=?, venue=?, capacity=?, logo_path=?,
                                                final_entry_time=?, end_time=?, end_date=?
                                            WHERE id=?
                                        """, (
                                            new_name.strip(),
                                            str(new_date),
                                            new_time.strip(),
                                            new_venue.strip(),
                                            int(new_capacity),
                                            new_logo_path,
                                            new_final.strip(),
                                            new_end_time.strip(),
                                            str(new_end_date),
                                            eid
                                        ))
                                        conn.commit()
                                        close_connection(conn)
                                        st.session_state["event_updated"] = new_name.strip()
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to update event: {e}")
        else:
            st.warning("No events found.")
    except Exception as e:
        st.error(f"Error loading events: {e}")

# --- USERS PAGE ---
# --- USERS PAGE (defensive created_at on registrations) ---
elif page == "Users":
    st.header("👥 User Management")
    st.info("View registered users. CSV export has masked Aadhaar for privacy.")

    col_u1, col_u2 = st.columns([3, 2])
    with col_u1:
        user_q = st.text_input("Search users by name or email", key="user_q")
    with col_u2:
        filter_event = st.selectbox("Event (optional)", ["All"], key="user_event_filter")
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            cursor.execute("SELECT DISTINCT name FROM events ORDER BY name ASC")
            event_names = [r[0] for r in cursor.fetchall()]
            close_connection(conn)
            if event_names:
                options = ["All"] + event_names
                idx = options.index(st.session_state.get("user_event_filter", "All")) if st.session_state.get("user_event_filter", "All") in options else 0
                filter_event = st.selectbox("Event (optional)", options, index=idx, key="user_event_filter")
        except Exception:
            pass

    try:
        has_reg_created_at = _has_column("registrations", "created_at")

        base_select = """
            SELECT u.name, u.email, u.aadhar_number,
                   e.name AS event_name, r.pass_id{created_at_sel}
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            JOIN events e ON r.event_id = e.id
            WHERE 1=1
        """
        created_at_sel = ", r.created_at" if has_reg_created_at else ""
        user_query = base_select.format(created_at_sel=created_at_sel)

        user_params = []
        if user_q:
            user_query += " AND (u.name LIKE ? OR u.email LIKE ?)"
            user_params += [f"%{user_q}%", f"%{user_q}%"]
        if filter_event and filter_event != "All":
            user_query += " AND e.name = ?"
            user_params.append(filter_event)

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(user_query, tuple(user_params))
        users = cursor.fetchall()
        close_connection(conn)

        if users:
            st.subheader("Registered users")
            display_rows = []
            csv_rows = []

            for r in users:
                if has_reg_created_at and len(r) == 6:
                    name, email, aadhar, event, pass_id, created_at = r
                else:
                    name, email, aadhar, event, pass_id = r
                    created_at = ""

                display_rows.append([name, email, _mask_aadhaar(aadhar), event, pass_id])
                csv_rows.append([name, email, _mask_aadhaar(aadhar), event, pass_id, created_at])

            st.table(display_rows)

            headers = ["Name", "Email", "Aadhaar_masked", "Event", "Pass ID", "Created At"]
            now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_name = f"users_export_{now}.csv"
            csv_text = _to_csv_string(csv_rows, headers)
            csv_bytes = csv_text.encode("utf-8")
            st.caption("Aadhaar is masked in the display and export. Full Aadhaar remains in the DB for admin-only ops.")
            _download_button_bytes("⬇️ Export users (CSV, masked Aadhaar)", csv_bytes, file_name)
            _log_export(admin_user=st.session_state.get("username", "admin"),
                        export_type="users_masked_aadhaar",
                        row_count=len(csv_rows),
                        file_name=file_name)
        else:
            st.warning("No users found for the current filter.")
    except Exception as e:
        st.error(f"Error loading users: {e}")

# --- PASSES PAGE ---
# --- PASSES PAGE (defensive generated_at on registrations) ---
elif page == "Passes":
    st.header("🎟️ Pass Overview")
    st.info("View generated passes and export CSV.")

    col_p1, col_p2 = st.columns([3, 2])
    with col_p1:
        pass_q = st.text_input("Search passes by name or pass id", key="pass_q")
    with col_p2:
        pass_event = st.selectbox("Event (optional)", ["All"], key="pass_event_filter")
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            cursor.execute("SELECT DISTINCT name FROM events ORDER BY name ASC")
            pass_event_names = [r[0] for r in cursor.fetchall()]
            close_connection(conn)
            if pass_event_names:
                options = ["All"] + pass_event_names
                idx = options.index(st.session_state.get("pass_event_filter", "All")) if st.session_state.get("pass_event_filter", "All") in options else 0
                pass_event = st.selectbox("Event (optional)", options, index=idx, key="pass_event_filter")
        except Exception:
            pass

    try:
        has_reg_generated_at = _has_column("registrations", "generated_at")

        base_select = """
            SELECT u.name, e.name AS event_name, r.pass_id{generated_at_sel}
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            JOIN events e ON r.event_id = e.id
            WHERE 1=1
        """
        generated_at_sel = ", r.generated_at" if has_reg_generated_at else ""
        pass_query = base_select.format(generated_at_sel=generated_at_sel)

        pass_params = []
        if pass_q:
            pass_query += " AND (u.name LIKE ? OR r.pass_id LIKE ?)"
            pass_params += [f"%{pass_q}%", f"%{pass_q}%"]
        if pass_event and pass_event != "All":
            pass_query += " AND e.name = ?"
            pass_params.append(pass_event)

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(pass_query, tuple(pass_params))
        passes = cursor.fetchall()
        close_connection(conn)

        if passes:
            st.subheader("Passes (preview first 10 rows)")
            preview = []
            csv_rows = []

            for r in passes[:10]:
                if has_reg_generated_at and len(r) == 4:
                    name, event, pid, gen_at = r
                else:
                    name, event, pid = r
                    gen_at = ""
                preview.append([name, event, pid, gen_at])

            st.table(preview)

            for r in passes:
                if has_reg_generated_at and len(r) == 4:
                    name, event, pid, gen_at = r
                else:
                    name, event, pid = r
                    gen_at = ""
                csv_rows.append([name, event, pid, gen_at])

            headers = ["Name", "Event", "Pass ID", "Pass Generated At"]
            now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_name = f"passes_export_{now}.csv"
            csv_text = _to_csv_string(csv_rows, headers)
            csv_bytes = csv_text.encode("utf-8")
            st.caption("Pass CSV contains pass IDs. Handle with care.")
            _download_button_bytes("⬇️ Export passes (CSV)", csv_bytes, file_name)
            _log_export(admin_user=st.session_state.get("username", "admin"),
                        export_type="passes",
                        row_count=len(csv_rows),
                        file_name=file_name)
        else:
            st.warning("No passes found for the current filter.")
    except Exception as e:
        st.error(f"Error loading passes: {e}")

# --- GENERATE PASS PAGE ---
elif page == "Generate Pass":
    st.header("🔑 Generate Pass (Admin Only)")
    st.info("Admins can regenerate a pass by Aadhaar number only.")

    aadhar_input = st.text_input("Enter Aadhaar Number")
    if st.button("Generate Pass"):
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            cursor.execute("""
                SELECT r.pass_id, u.name, e.name AS event_name
                FROM registrations r
                JOIN users u ON r.user_id = u.user_id
                JOIN events e ON r.event_id = e.id
                WHERE u.aadhar_number = ?
            """, (aadhar_input,))
            user = cursor.fetchone()
            close_connection(conn)

            if user:
                pass_id, name, event = user
                pdf_path = os.path.join(PASS_PDF_DIR, f"{pass_id}.pdf")
                try:
                    with open(pdf_path, "rb") as f:
                        st.download_button("📄 Download Pass", f, file_name=f"{pass_id}.pdf")
                except:
                    st.warning("Pass PDF not found. It may need regeneration.")
            else:
                st.error("No pass found for that Aadhaar number.")
        except Exception as e:
            st.error(f"Error generating pass: {e}")

# --- VERIFY PASS PAGE ---
elif page == "Verify Pass":
    st.header("🔍 Verify Pass")
    st.info("Validate a pass by Pass ID and optionally verify Aadhaar.")

    pass_id_in = st.text_input("Pass ID", key="verify_pass_id")
    aadhaar_in = st.text_input("Aadhaar (optional)", key="verify_aadhaar")
    if st.button("Verify", key="verify_btn"):
        if not pass_id_in:
            st.error("Enter a Pass ID.")
        else:
            try:
                conn = get_connection()
                cursor = get_cursor(conn)
                cursor.execute("""
                    SELECT u.name, u.aadhar_number, e.name AS event_name, r.pass_id,
                           e.status, e.final_entry_time, e.end_time, e.end_date
                    FROM registrations r
                    JOIN users u ON r.user_id = u.user_id
                    JOIN events e ON r.event_id = e.id
                    WHERE r.pass_id = ?
                """, (pass_id_in.strip(),))
                row = cursor.fetchone()
                close_connection(conn)

                if not row:
                    st.error("Invalid pass.")
                else:
                    uname, uaadhaar, uevent, upassid, estatus, efinal, eend, eend_date = row
                    if aadhaar_in and aadhaar_in.strip() != (uaadhaar or "").strip():
                        st.error("Aadhaar does not match this pass.")
                    else:
                        st.success("Pass valid.")
                        st.write(f"**Name:** {uname}")
                        st.write(f"**Event:** {uevent}")
                        st.write(f"**Pass ID:** {upassid}")
                        st.write(f"**Event Status:** {estatus}")
                        st.caption(f"Final entry: {efinal} • Ends: {eend} • End date: {eend_date}")
            except Exception as e:
                st.error(f"Error verifying pass: {e}")