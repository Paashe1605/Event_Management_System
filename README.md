
---

# 🎪 Next-Gen Event Management System (EMS) 🚀

**Elevating Event Experiences through Intelligent Automation & Seamless Management**

A robust, full-stack Python application designed to handle everything from user registrations and secure login to dynamic QR-coded event pass generation and administrative auditing.


---

## ✨ Key Features

* 🔐 **Secure Role-Based Access Control (RBAC):** Dedicated views and permissions for standard Users and Administrators.
* 🎟️ **Smart Pass Generation:** Automatically generate high-quality PDF passes for registered attendees.
* 📱 **Dynamic QR Code Integration:** Every pass comes with a unique, scannable QR code for secure, frictionless event check-ins.
* 📊 **Comprehensive Admin Dashboard:** A centralized hub to monitor active events, track registrations, and manage users.
* 🕵️ **Encrypted Audit Trails:** Built-in logging with encrypted CSV exports (`decrypt_csv.py`) to ensure data integrity and compliance.
* 🎨 **Sleek Multi-Page UI:** A fluid, intuitive user experience separated cleanly into logical pages (Home, Login, Register, My Pass).

---

## 🛠️ Tech Stack

* **Core:** Python 3.x
* **Frontend / UI:** Streamlit *(Inferred via multi-page structure)*
* **Database:** SQLite3 (`event_management.db`)
* **Assets & Media:** Dynamic Image Processing & PDF Generation
* **Security:** Cryptographic utilities for log management

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python 3.9+ installed on your system.

```bash
python --version

```

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/event_management_system.git
cd event_management_system

```

**2. Create a virtual environment (Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

**3. Install dependencies**
*(Assuming a requirements.txt is present. If not, install your specific packages like streamlit, fpdf, qrcode, etc.)*

```bash
pip install -r requirements.txt

```

**4. Initialize the Database**
Run the initial setup to construct the tables.

```bash
python setup.py
# Or run the specific migration files if needed:
python services/migrations/create_events_table.py

```

**5. Launch the Application**

```bash
streamlit run app.py 

```

---

## 📂 Project Structure

A clean, modular architecture separating the data layer, presentation layer, and business logic.

```text
📦 Event_Management_System
 ┣ 📂 assets                  # Static media, logos, and generated outputs
 ┃ ┣ 📂 audit                 # Exported audit logs (CSV)
 ┃ ┣ 📂 logos                 # Event banners and images
 ┃ ┣ 📂 passes                # Dynamically generated PDF tickets
 ┃ ┗ 📂 qrcodes               # Generated QR codes for tickets
 ┣ 📂 data                    # Local SQLite database stores
 ┣ 📂 models                  # Data schemas and object representations
 ┃ ┣ 📜 event.py
 ┃ ┗ 📜 user.py
 ┣ 📂 pages                   # Multi-page application routing
 ┃ ┣ 📜 admin_dashboard.py    # Admin control center
 ┃ ┣ 📜 home.py               # Landing page & event browsing
 ┃ ┣ 📜 login.py              # User authentication
 ┃ ┣ 📜 my_pass.py            # User ticket retrieval
 ┃ ┗ 📜 register.py           # New user onboarding
 ┣ 📂 services                # Core business logic and database interactions
 ┃ ┣ 📂 migrations            # Schema updates and fixes
 ┃ ┗ 📜 database.py           # DB connection engine
 ┣ 📜 app.py                  # Main application entry point
 ┣ 📜 db.py                   # Database utility scripts
 ┣ 📜 decrypt_csv.py          # Security utility for audit logs
 ┗ 📜 setup.py                # Initial configuration script

```

---

---

## 🔒 Security & Data Integrity

This project takes data seriously.

* **Database Migrations:** The `updates_archives/` folder tracks historic schema changes (e.g., adding roles, tracking pass IDs) to ensure safe versioning.
* **Audit Logging:** Critical actions are logged to `assets/audit/export_log.csv`.
* **Decryption:** The `decrypt_csv.py` script ensures that sensitive log exports remain secure at rest and can only be accessed by authorized administrators.

---

## 🤝 Contributing

Contributions make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---