# SkillLoop Bharat — Prototype Implementation

> **"Learn from Real Problems. Build Real Skills."**

SkillLoop Bharat is a college-managed web platform where nearby local businesses share small, real-world operational problems. The college coordinator reviews and approves the challenges, student teams build practical solutions under the guidance of assigned faculty mentors, and partner businesses provide direct evaluation and feedback.

---

## 🌟 Key Prototype Highlights & Features

### 1. Four Fully Interactive User Roles
- **👨‍🎓 Student (Aarav Sharma — 3rd Year B.Tech):** Browse approved tasks, join available problems, submit prototype solutions with repo links and documentation, and view a verified project portfolio.
- **🏢 Company Representative (Rajesh Gupta — Green Basket Stores):** Submit new business challenges, track college vetting, inspect submitted student prototypes, and submit qualitative feedback and star ratings.
- **👩‍🏫 Faculty Mentor (Dr. Sunita Rao — Dept. of Computer Engineering):** Guide students, review submitted source code and architecture, and authorize work with academic feedback.
- **🏛️ College Coordinator (Prof. K. V. Raman — Head, Industry Relations):** Vets company submissions, ensures curriculum alignment, assigns domain faculty mentors, and tracks campus-wide innovation metrics.

### 2. 1-Click Role Switcher & Live Presentation Bar
- Built specifically for demo presentations and judges: switch between all 4 personas in a single click from the sticky top navigation bar without needing separate logins.
- Includes a 6-step lifecycle tracker bar guiding viewers through the full company-to-student journey.
- **Reset Sample Data** button instantly restores the SQLite database back to initial pristine demo state anytime.

### 3. Realistic Demo Data Pre-Seeded
- **Completed Showcase:** *"Simple Stock Tracker for a Local Grocery Shop"* (Green Basket Stores) — Full lifecycle with working prototype, faculty review, and 5-star company testimonial.
- **Approved & Open Task:** *"Bilingual QR Code Menu & Table Ordering"* (Annapurna Bhavan Veg Diner) — Ready for the student to join and submit live during presentation!
- **Pending Approval Challenge:** *"Handloom Artisan Product Catalog & WhatsApp Enquiry Bot"* (Kashi Weavers Cooperative Society) — Ready for the College Coordinator to approve and assign a mentor live!
- **Active Task:** *"School Bus Delay Alert System"* (Shanti Public School) — In-progress student project.

---

## 🚀 Quick Start Guide

### Running via the launcher
Simply double-click or run:
```powershell
.\run.ps1
```
or in Command Prompt:
```cmd
run.bat
```

### Running directly with uv & Python
```bash
uv run --with flask python app.py
```

The web application will launch at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🎬 6-Step Presentation Walkthrough Script

Follow this sequence to deliver a high-impact presentation to judges:

1. **Welcome Page & Vision (`/`):**
   - Introduce the core problem: Students graduate with theory but lack real-world problem-solving practice; local businesses have small operational problems but lack engineering budgets.
   - Show the 4 role cards and the live statistics cards.

2. **Company Posts a Problem (`Company Dashboard`):**
   - Switch to **🏢 Company** via top demo bar.
   - Click **"Share New Problem Form"** to show how a local business (e.g. Kirana store, restaurant, school) can post a 1-page challenge in 2 minutes.

3. **College Approval & Mentorship Assignment (`College Approvals`):**
   - Switch to **🏛️ College Coordinator**.
   - Show the Pending Approval queue (e.g. *Kashi Weavers Cooperative*).
   - Click **"Approve & Assign Mentor"** (assign Dr. Sunita Rao).
   - Point out how this prevents spam and ensures academic credit.

4. **Student Joins & Submits Solution (`Student Hub`):**
   - Switch to **👨‍🎓 Student** (Aarav Sharma).
   - In "Available Approved Problems", click **"View & Join Task"** on the newly approved problem or *Annapurna Bhavan QR Menu*.
   - Click **"Join This Problem"** — notice the status changes immediately to **In Progress**!
   - Fill the **"Submit Your Solution"** form with demo URL and summary.

5. **Faculty Guidance & Review (`Faculty Mentoring`):**
   - Switch to **👩‍🏫 Faculty Mentor** (Dr. Sunita Rao).
   - View the student's submission, enter qualitative feedback, and select **"Reviewed"**.

6. **Company Feedback & Verified Portfolio (`Student Portfolio`):**
   - Switch to **🏢 Company** and submit a 5-star review and encouraging testimonial.
   - Open **🎓 Student Portfolio** (`/portfolio`): View the student's verified project showcase with problem context, technical contribution, faculty mentor validation, and authentic business testimonial!

---

## 🛠️ Architecture & Tech Stack

- **Frontend:** Responsive HTML5, Custom CSS3 Design System with Indian modern aesthetic (Navy Blue `#0F172A`, Teal `#0D9488`, Saffron Orange `#EA580C`, Emerald `#059669`), Vanilla JavaScript for modal and tab interactions.
- **Backend:** Python Flask 3.1 lightweight web application.
- **Database:** SQLite (`skillloop.db`) with tables for problems, submissions, reviews, and audit timestamps.
- **Zero Complex External Dependencies:** Runs natively with standard Python packages and `uv`.
