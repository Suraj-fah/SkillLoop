import os
import sqlite3
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g

app = Flask(__name__)
app.secret_key = "skillloop-bharat-demo-secret-key-2026"

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skillloop.db")

# Demo Users
DEMO_USERS = {
    "student": {
        "id": 1,
        "role": "student",
        "name": "Aarav Sharma",
        "title": "3rd Year B.Tech Computer Engineering",
        "institution": "Bharat Institute of Technology, Pune",
        "avatar": "👨‍🎓",
        "email": "aarav.sharma@bitpune.ac.in",
        "skills": "Python, Web Development, UI/UX, Problem Solving"
    },
    "company": {
        "id": 2,
        "role": "company",
        "name": "Rajesh Gupta",
        "title": "Operations Manager",
        "company_name": "Green Basket Stores",
        "institution": "Green Basket Stores (Retail & Daily Essentials)",
        "avatar": "🏢",
        "email": "rajesh@greenbasket.in",
        "location": "Pune, Maharashtra"
    },
    "faculty": {
        "id": 3,
        "role": "faculty",
        "name": "Dr. Sunita Rao",
        "title": "Associate Professor, Dept. of Computer Engineering",
        "institution": "Bharat Institute of Technology, Pune",
        "avatar": "👩‍🏫",
        "email": "sunita.rao@bitpune.ac.in",
        "specialization": "Information Systems & Applied Software"
    },
    "coordinator": {
        "id": 4,
        "role": "coordinator",
        "name": "Prof. K. V. Raman",
        "title": "Head, Industry Relations & Skill Cell",
        "institution": "Bharat Institute of Technology, Pune",
        "avatar": "🏛️",
        "email": "kv.raman@bitpune.ac.in",
        "office": "Dean of Academic-Industry Linkages"
    }
}

DEMO_FACULTY_LIST = [
    {"id": 3, "name": "Dr. Sunita Rao", "dept": "Computer Engineering", "specialization": "Software & Web Systems"},
    {"id": 5, "name": "Prof. Anand Deshmukh", "dept": "Mechanical & Operations", "specialization": "Supply Chain & IoT"},
    {"id": 6, "name": "Dr. Meenakshi Iyer", "dept": "Data Science & AI", "specialization": "Business Analytics & Databases"}
]

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db(force_reseed=False):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    if force_reseed:
        cursor.execute("DROP TABLE IF EXISTS problems")
        cursor.execute("DROP TABLE IF EXISTS submissions")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company_name TEXT NOT NULL,
        company_contact TEXT,
        topic TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Moderate',
        description TEXT NOT NULL,
        student_task TEXT NOT NULL,
        expected_result TEXT NOT NULL,
        required_skills TEXT NOT NULL,
        deadline TEXT NOT NULL,
        status TEXT NOT NULL, -- 'Pending Approval', 'Needs Changes', 'Approved', 'In Progress', 'Submitted', 'Reviewed', 'Completed', 'Rejected'
        faculty_mentor_id INTEGER,
        faculty_mentor_name TEXT,
        assigned_student_id INTEGER,
        assigned_student_name TEXT,
        coordinator_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        submission_title TEXT NOT NULL,
        solution_summary TEXT NOT NULL,
        demo_url TEXT,
        github_repo TEXT,
        files_attached TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        faculty_feedback TEXT,
        faculty_status TEXT, -- 'Reviewed', 'Changes Needed'
        faculty_reviewed_at TIMESTAMP,
        company_feedback TEXT,
        company_rating INTEGER, -- 1 to 5
        company_feedback_at TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems (id)
    )
    """)

    db.commit()

    # Check if seed data exists
    cursor.execute("SELECT COUNT(*) FROM problems")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_sample_data(db)

    db.close()

def seed_sample_data(db):
    cursor = db.cursor()

    # Problem 1: Completed stock tracker project to show full lifecycle and student portfolio
    cursor.execute("""
    INSERT INTO problems (
        title, company_name, company_contact, topic, difficulty,
        description, student_task, expected_result, required_skills,
        deadline, status, faculty_mentor_id, faculty_mentor_name,
        assigned_student_id, assigned_student_name, coordinator_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Simple Stock Tracker for a Local Grocery Shop",
        "Green Basket Stores",
        "Rajesh Gupta (Operations Manager)",
        "Inventory & Retail Operations",
        "Beginner to Intermediate",
        "The shop finds it difficult to track which grocery products and daily essentials are running low. Current manual notebooks lead to stockouts during peak evening shopping hours.",
        "Suggest and build a simple, clean interface to list products, record remaining quantities, and trigger color-coded low-stock alerts before items run out.",
        "A working prototype demonstration or clear digital dashboard with 15-20 sample local grocery products and automatic reorder alerts.",
        "Problem-solving, basic Web Design (HTML/CSS/JS), teamwork, empathy for small businesses",
        "15 Nov 2026",
        "Completed",
        3,
        "Dr. Sunita Rao",
        1,
        "Aarav Sharma",
        "Approved. Very high practical relevance for local Kirana and departmental stores in Kothrud area."
    ))
    prob1_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO submissions (
        problem_id, student_id, student_name, submission_title,
        solution_summary, demo_url, github_repo, files_attached,
        submitted_at, faculty_feedback, faculty_status, faculty_reviewed_at,
        company_feedback, company_rating, company_feedback_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prob1_id,
        1,
        "Aarav Sharma",
        "KiranaTrack: Responsive Web Dashboard with Hindi & English Support",
        "Built a lightweight, mobile-first inventory tracker. It categorizes items (Grains, Dairy, Spices, Oils) with threshold alerts (Green = Safe, Yellow = Reorder soon, Red = Out of Stock). Includes 1-click WhatsApp order message generator to wholesale suppliers.",
        "https://kiranatrack-demo.skillloop.in",
        "https://github.com/aarav-sharma/kiranatrack-demo",
        "KiranaTrack_User_Manual.pdf, Architecture_Diagram.png",
        "2026-10-18 16:30:00",
        "Excellent execution by Aarav! The WhatsApp reorder button is a practical touch tailored to local vendor realities. Code is well-structured and clean. Ready for company evaluation.",
        "Reviewed",
        "2026-10-20 11:15:00",
        "“This is exactly what our store floor staff needed. It is so easy that even our non-tech helpers can update stock in 10 seconds. We are planning a pilot next week!”",
        5,
        "2026-10-21 14:00:00"
    ))

    # Problem 2: An Approved problem waiting for student to join!
    cursor.execute("""
    INSERT INTO problems (
        title, company_name, company_contact, topic, difficulty,
        description, student_task, expected_result, required_skills,
        deadline, status, faculty_mentor_id, faculty_mentor_name,
        assigned_student_id, assigned_student_name, coordinator_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Bilingual QR Code Menu & Table Ordering for Annapurna Bhavan",
        "Annapurna Bhavan Veg Diner",
        "Suresh Kulkarni (Managing Partner)",
        "Hospitality Tech & Localization",
        "Moderate",
        "During lunch hours, elderly diners and college students crowd the counter. Printed menus get dirty and price updates require frequent reprinting.",
        "Design a lightweight mobile web menu in Marathi and English that customers can open by scanning a QR sticker on their dining table.",
        "A responsive mobile web page with category tabs (Thalis, Snacks, Beverages), bilingual item descriptions, and estimated wait times.",
        "Front-end Web Development, Regional Language Typography, Mobile UX",
        "30 Nov 2026",
        "Approved",
        3,
        "Dr. Sunita Rao",
        None,
        None,
        "Approved. High community utility. Assigned to Dr. Sunita Rao for web guidance."
    ))

    # Problem 3: A newly submitted problem waiting for College Coordinator Approval!
    cursor.execute("""
    INSERT INTO problems (
        title, company_name, company_contact, topic, difficulty,
        description, student_task, expected_result, required_skills,
        deadline, status, faculty_mentor_id, faculty_mentor_name,
        assigned_student_id, assigned_student_name, coordinator_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Handloom Artisan Product Catalog & WhatsApp Enquiry Bot",
        "Kashi Weavers Cooperative Society",
        "Rameshwar Prasad (Secretary)",
        "E-Commerce & Digital Inclusion",
        "Moderate",
        "Traditional handloom weavers want to showcase authentic sarees and stoles to urban buyers directly, without losing 40% margin to middleman platforms.",
        "Create a visual web catalog showcasing artisan stories, authentic weave photos, and a simple 'Enquire via WhatsApp' button with preset product codes.",
        "Interactive web catalog with product gallery, weaver profile cards, and direct WhatsApp chat links with pre-filled product details.",
        "Web Design, Visual Storytelling, WhatsApp Click-to-Chat API",
        "10 Dec 2026",
        "Pending Approval",
        None,
        None,
        None,
        None,
        None
    ))

    # Problem 4: Active in-progress problem
    cursor.execute("""
    INSERT INTO problems (
        title, company_name, company_contact, topic, difficulty,
        description, student_task, expected_result, required_skills,
        deadline, status, faculty_mentor_id, faculty_mentor_name,
        assigned_student_id, assigned_student_name, coordinator_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "School Bus Morning Delay SMS & Telegram Alert System",
        "Shanti Public School & Transport Association",
        "Meena Patil (School Administrator)",
        "Community Safety & Communication",
        "Beginner to Intermediate",
        "When school buses get stuck in morning traffic or waterlogging during rains, parents panic and overwhelm the school telephone lines.",
        "Design a quick 1-click broadcast notification interface where the bus in-charge can dispatch route delay updates to parents.",
        "A prototype admin dashboard to select a bus route and trigger pre-formatted SMS/Telegram alert templates.",
        "UI Design, Basic Python/JavaScript, Notification APIs",
        "05 Dec 2026",
        "In Progress",
        3,
        "Dr. Sunita Rao",
        1,
        "Aarav Sharma",
        "Approved with priority due to student safety importance."
    ))

    db.commit()

# Current User helper
@app.context_processor
def inject_globals():
    role = session.get("role", "student")
    user = DEMO_USERS.get(role, DEMO_USERS["student"])
    return {
        "current_user": user,
        "active_role": role,
        "all_roles": DEMO_USERS,
        "faculty_list": DEMO_FACULTY_LIST,
        "now_date": date.today().strftime("%d %b %Y")
    }

# ----------------- ROUTES ----------------- #

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM problems WHERE status IN ('Approved', 'In Progress', 'Submitted', 'Reviewed', 'Completed')")
    approved_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems WHERE status = 'Completed'")
    completed_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems")
    total_count = cursor.fetchone()[0]

    # Get sample approved problems for landing page
    cursor.execute("""
        SELECT * FROM problems 
        WHERE status IN ('Approved', 'In Progress', 'Completed') 
        ORDER BY id DESC LIMIT 3
    """)
    sample_problems = cursor.fetchall()

    return render_template("index.html", 
                           approved_count=approved_count, 
                           completed_count=completed_count, 
                           total_count=total_count,
                           sample_problems=sample_problems)

@app.route("/switch-role/<role>")
def switch_role(role):
    if role in DEMO_USERS:
        session["role"] = role
        flash(f"Switched role to {DEMO_USERS[role]['name']} ({role.capitalize()})", "info")
    
    # Redirect to corresponding dashboard
    if role == "student":
        return redirect(url_for("student_dashboard"))
    elif role == "company":
        return redirect(url_for("company_dashboard"))
    elif role == "faculty":
        return redirect(url_for("faculty_dashboard"))
    elif role == "coordinator":
        return redirect(url_for("coordinator_dashboard"))
    return redirect(url_for("index"))

@app.route("/reset-demo-data", methods=["POST", "GET"])
def reset_demo_data():
    init_db(force_reseed=True)
    flash("Demo database has been restored to standard initial state!", "success")
    return redirect(request.referrer or url_for("index"))

# ----------------- STUDENT ----------------- #

@app.route("/student")
def student_dashboard():
    session["role"] = "student"
    db = get_db()
    cursor = db.cursor()

    # Available problems: Approved problems that haven't been joined yet
    cursor.execute("""
        SELECT * FROM problems 
        WHERE status = 'Approved' AND assigned_student_id IS NULL
        ORDER BY id DESC
    """)
    available_problems = cursor.fetchall()

    # Joined problems: In Progress or Submitted or Reviewed
    cursor.execute("""
        SELECT p.*, s.submission_title, s.submitted_at, s.faculty_feedback, s.faculty_status, s.company_feedback, s.company_rating
        FROM problems p
        LEFT JOIN submissions s ON p.id = s.problem_id
        WHERE p.assigned_student_id = ? AND p.status IN ('In Progress', 'Submitted', 'Reviewed')
        ORDER BY p.id DESC
    """, (DEMO_USERS["student"]["id"],))
    joined_problems = cursor.fetchall()

    # Completed problems
    cursor.execute("""
        SELECT p.*, s.submission_title, s.submitted_at, s.faculty_feedback, s.company_feedback, s.company_rating
        FROM problems p
        JOIN submissions s ON p.id = s.problem_id
        WHERE p.assigned_student_id = ? AND p.status = 'Completed'
        ORDER BY p.id DESC
    """, (DEMO_USERS["student"]["id"],))
    completed_problems = cursor.fetchall()

    return render_template("student_dashboard.html",
                           available_problems=available_problems,
                           joined_problems=joined_problems,
                           completed_problems=completed_problems)

@app.route("/portfolio")
@app.route("/portfolio/<int:student_id>")
def student_portfolio(student_id=None):
    if student_id is None:
        student_id = DEMO_USERS["student"]["id"]
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.*, s.submission_title, s.solution_summary, s.demo_url, s.github_repo,
               s.files_attached, s.submitted_at, s.faculty_feedback, s.faculty_status,
               s.faculty_reviewed_at, s.company_feedback, s.company_rating, s.company_feedback_at
        FROM problems p
        JOIN submissions s ON p.id = s.problem_id
        WHERE p.assigned_student_id = ? AND p.status = 'Completed'
        ORDER BY s.company_feedback_at DESC, p.id DESC
    """, (student_id,))
    portfolio_projects = cursor.fetchall()

    return render_template("portfolio.html", projects=portfolio_projects)

# ----------------- PROBLEM DETAILS & ACTIONS ----------------- #

@app.route("/problem/<int:problem_id>")
def problem_detail(problem_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
    problem = cursor.fetchone()

    if not problem:
        flash("Problem not found.", "error")
        return redirect(url_for("index"))

    cursor.execute("""
        SELECT * FROM submissions 
        WHERE problem_id = ? 
        ORDER BY id DESC LIMIT 1
    """, (problem_id,))
    submission = cursor.fetchone()

    return render_template("problem_detail.html", problem=problem, submission=submission)

@app.route("/problem/<int:problem_id>/join", methods=["POST"])
def join_problem(problem_id):
    db = get_db()
    cursor = db.cursor()
    student = DEMO_USERS["student"]

    cursor.execute("""
        UPDATE problems 
        SET status = 'In Progress', 
            assigned_student_id = ?, 
            assigned_student_name = ?
        WHERE id = ? AND status = 'Approved'
    """, (student["id"], student["name"], problem_id))
    db.commit()

    flash(f"🎉 You have joined this real-world task! You can now start working with your faculty mentor {problem_id}.", "success")
    return redirect(url_for("problem_detail", problem_id=problem_id))

@app.route("/problem/<int:problem_id>/submit", methods=["POST"])
def submit_solution(problem_id):
    db = get_db()
    cursor = db.cursor()
    student = DEMO_USERS["student"]

    title = request.form.get("submission_title", "").strip()
    summary = request.form.get("solution_summary", "").strip()
    demo_url = request.form.get("demo_url", "").strip()
    github_repo = request.form.get("github_repo", "").strip()
    files_attached = request.form.get("files_attached", "Documentation_Overview.pdf")

    if not title or not summary:
        flash("Please provide a title and summary of your solution.", "error")
        return redirect(url_for("problem_detail", problem_id=problem_id))

    cursor.execute("""
        INSERT INTO submissions (
            problem_id, student_id, student_name, submission_title,
            solution_summary, demo_url, github_repo, files_attached
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (problem_id, student["id"], student["name"], title, summary, demo_url, github_repo, files_attached))

    cursor.execute("""
        UPDATE problems 
        SET status = 'Submitted' 
        WHERE id = ?
    """, (problem_id,))
    db.commit()

    flash("🚀 Solution submitted successfully! Your faculty mentor has been notified for review.", "success")
    return redirect(url_for("problem_detail", problem_id=problem_id))

# ----------------- COMPANY ----------------- #

@app.route("/company")
def company_dashboard():
    session["role"] = "company"
    db = get_db()
    cursor = db.cursor()

    company_name = DEMO_USERS["company"]["company_name"]
    cursor.execute("""
        SELECT p.*, s.id as submission_id, s.submission_title, s.solution_summary, 
               s.demo_url, s.faculty_feedback, s.faculty_status, s.company_feedback, s.company_rating
        FROM problems p
        LEFT JOIN submissions s ON p.id = s.problem_id
        WHERE p.company_name = ? OR p.company_name LIKE ?
        ORDER BY p.id DESC
    """, (company_name, f"%{company_name}%"))
    problems = cursor.fetchall()

    return render_template("company_dashboard.html", problems=problems)

@app.route("/company/post-problem", methods=["POST"])
def post_problem():
    title = request.form.get("title", "").strip()
    topic = request.form.get("topic", "").strip()
    difficulty = request.form.get("difficulty", "Moderate")
    description = request.form.get("description", "").strip()
    student_task = request.form.get("student_task", "").strip()
    expected_result = request.form.get("expected_result", "").strip()
    required_skills = request.form.get("required_skills", "").strip()
    deadline = request.form.get("deadline", "15 Dec 2026").strip()
    company_name = request.form.get("company_name", DEMO_USERS["company"]["company_name"]).strip()
    company_contact = f"{DEMO_USERS['company']['name']} ({DEMO_USERS['company']['title']})"

    if not title or not description:
        flash("Please fill in the problem title and description.", "error")
        return redirect(url_for("company_dashboard"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO problems (
            title, company_name, company_contact, topic, difficulty,
            description, student_task, expected_result, required_skills,
            deadline, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending Approval')
    """, (title, company_name, company_contact, topic, difficulty,
          description, student_task, expected_result, required_skills, deadline))
    db.commit()

    flash("✅ Problem submitted to Bharat Institute of Technology for approval! The College Coordinator will review it.", "success")
    return redirect(url_for("company_dashboard"))

@app.route("/company/give-feedback/<int:problem_id>", methods=["POST"])
def give_company_feedback(problem_id):
    feedback = request.form.get("company_feedback", "").strip()
    rating = int(request.form.get("company_rating", 5))

    if not feedback:
        flash("Please enter feedback for the student team.", "error")
        return redirect(url_for("company_dashboard"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE submissions 
        SET company_feedback = ?, 
            company_rating = ?, 
            company_feedback_at = CURRENT_TIMESTAMP
        WHERE problem_id = ?
    """, (feedback, rating, problem_id))

    cursor.execute("""
        UPDATE problems 
        SET status = 'Completed' 
        WHERE id = ?
    """, (problem_id,))
    db.commit()

    flash("🌟 Thank you! Company feedback recorded and project marked Completed in student's verified portfolio.", "success")
    return redirect(url_for("company_dashboard"))

# ----------------- COLLEGE COORDINATOR ----------------- #

@app.route("/coordinator")
def coordinator_dashboard():
    session["role"] = "coordinator"
    db = get_db()
    cursor = db.cursor()

    # Pending problems waiting for review
    cursor.execute("""
        SELECT * FROM problems 
        WHERE status = 'Pending Approval' 
        ORDER BY id DESC
    """)
    pending_problems = cursor.fetchall()

    # All active / approved problems
    cursor.execute("""
        SELECT * FROM problems 
        WHERE status != 'Pending Approval' 
        ORDER BY id DESC
    """)
    all_problems = cursor.fetchall()

    # Stats
    cursor.execute("SELECT COUNT(*) FROM problems WHERE status IN ('Approved', 'In Progress', 'Submitted', 'Reviewed')")
    active_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems WHERE status = 'Completed'")
    completed_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems WHERE status = 'Pending Approval'")
    pending_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM problems")
    total_count = cursor.fetchone()[0]

    return render_template("coordinator_dashboard.html",
                           pending_problems=pending_problems,
                           all_problems=all_problems,
                           active_count=active_count,
                           completed_count=completed_count,
                           pending_count=pending_count,
                           total_count=total_count)

@app.route("/coordinator/moderate/<int:problem_id>", methods=["POST"])
def moderate_problem(problem_id):
    action = request.form.get("action")
    mentor_id = request.form.get("faculty_mentor_id")
    notes = request.form.get("coordinator_notes", "").strip()

    db = get_db()
    cursor = db.cursor()

    if action == "approve":
        # Find mentor name
        mentor_name = "Dr. Sunita Rao"
        for m in DEMO_FACULTY_LIST:
            if str(m["id"]) == str(mentor_id):
                mentor_name = m["name"]
                break

        cursor.execute("""
            UPDATE problems 
            SET status = 'Approved', 
                faculty_mentor_id = ?, 
                faculty_mentor_name = ?, 
                coordinator_notes = ? 
            WHERE id = ?
        """, (mentor_id or 3, mentor_name, notes or "Approved for academic curriculum credit.", problem_id))
        flash(f"✅ Problem #{problem_id} approved! Faculty mentor {mentor_name} has been assigned.", "success")

    elif action == "request_changes":
        cursor.execute("""
            UPDATE problems 
            SET status = 'Needs Changes', 
                coordinator_notes = ? 
            WHERE id = ?
        """, (notes or "Scope needs to be adjusted for undergraduate student semester timeline.", problem_id))
        flash(f"⚠️ Requested modifications for Problem #{problem_id}.", "warning")

    elif action == "reject":
        cursor.execute("""
            UPDATE problems 
            SET status = 'Rejected', 
                coordinator_notes = ? 
            WHERE id = ?
        """, (notes or "Not aligned with current department project guidelines.", problem_id))
        flash(f"❌ Problem #{problem_id} rejected.", "info")

    db.commit()
    return redirect(url_for("coordinator_dashboard"))

# ----------------- FACULTY MENTOR ----------------- #

@app.route("/faculty")
def faculty_dashboard():
    session["role"] = "faculty"
    db = get_db()
    cursor = db.cursor()

    mentor_id = DEMO_USERS["faculty"]["id"]

    # Student projects assigned to this faculty mentor
    cursor.execute("""
        SELECT p.*, s.id as submission_id, s.student_name, s.submission_title, 
               s.solution_summary, s.demo_url, s.github_repo, s.files_attached,
               s.submitted_at, s.faculty_feedback, s.faculty_status, s.company_feedback, s.company_rating
        FROM problems p
        LEFT JOIN submissions s ON p.id = s.problem_id
        WHERE p.faculty_mentor_id = ? OR p.faculty_mentor_id IS NULL
        ORDER BY p.id DESC
    """, (mentor_id,))
    assigned_problems = cursor.fetchall()

    return render_template("faculty_dashboard.html", problems=assigned_problems)

@app.route("/faculty/review/<int:problem_id>", methods=["POST"])
def faculty_review(problem_id):
    feedback = request.form.get("faculty_feedback", "").strip()
    status = request.form.get("faculty_status", "Reviewed") # 'Reviewed' or 'Changes Needed'

    if not feedback:
        flash("Please enter evaluation notes for the student.", "error")
        return redirect(url_for("faculty_dashboard"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE submissions 
        SET faculty_feedback = ?, 
            faculty_status = ?, 
            faculty_reviewed_at = CURRENT_TIMESTAMP 
        WHERE problem_id = ?
    """, (feedback, status, problem_id))

    new_prob_status = "Reviewed" if status == "Reviewed" else "In Progress"
    cursor.execute("""
        UPDATE problems 
        SET status = ? 
        WHERE id = ?
    """, (new_prob_status, problem_id))

    db.commit()

    if status == "Reviewed":
        flash("🎓 Faculty review completed! The company can now view the solution and give feedback.", "success")
    else:
        flash("📝 Feedback sent to student requesting improvements before company review.", "info")

    return redirect(url_for("faculty_dashboard"))

if __name__ == "__main__":
    init_db()
    print("==============================================================")
    print("  SkillLoop Bharat Prototype Server Running!")
    print("  Learn from Real Problems. Build Real Skills.")
    print("  Open: http://127.0.0.1:5000 in your browser")
    print("==============================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
