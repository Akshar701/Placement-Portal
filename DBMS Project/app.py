import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from db import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")


def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session or session.get("role") != role:
                flash("Please login first.", "error")
                return redirect(url_for(f"{role}_login"))
            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT j.id, j.title, j.location, j.package_lpa, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        ORDER BY j.created_at DESC
        LIMIT 10
        """
    )
    jobs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", jobs=jobs)


@app.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        department = request.form["department"].strip()
        cgpa = request.form["cgpa"].strip()
        password = generate_password_hash(request.form["password"])

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO students (name, email, phone, department, cgpa, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, email, phone, department, cgpa, password),
            )
            conn.commit()
            flash("Student registration successful.", "success")
            return redirect(url_for("student_login"))
        except Exception as exc:
            conn.rollback()
            flash(f"Registration failed: {exc}", "error")
        finally:
            cur.close()
            conn.close()

    return render_template("student_register.html")


@app.route("/student/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE email = %s", (email,))
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student and check_password_hash(student["password_hash"], password):
            session["user_id"] = student["id"]
            session["name"] = student["name"]
            session["role"] = "student"
            flash("Welcome back!", "success")
            return redirect(url_for("student_dashboard"))

        flash("Invalid student credentials.", "error")

    return render_template("student_login.html")


@app.route("/student/dashboard")
@login_required("student")
def student_dashboard():
    student_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT j.id, j.title, j.location, j.package_lpa, c.company_name,
               EXISTS(
                 SELECT 1 FROM applications a
                 WHERE a.student_id = %s AND a.job_id = j.id
               ) AS already_applied
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        ORDER BY j.created_at DESC
        """,
        (student_id,),
    )
    jobs = cur.fetchall()

    cur.execute(
        """
        SELECT a.id, a.status, a.applied_at, j.title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE a.student_id = %s
        ORDER BY a.applied_at DESC
        """,
        (student_id,),
    )
    applications = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("student_dashboard.html", jobs=jobs, applications=applications)


@app.route("/student/apply/<int:job_id>", methods=["POST"])
@login_required("student")
def apply_job(job_id):
    student_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id FROM applications WHERE student_id = %s AND job_id = %s",
            (student_id, job_id),
        )
        if cur.fetchone():
            flash("You already applied for this job.", "error")
            return redirect(url_for("student_dashboard"))

        cur.execute(
            "INSERT INTO applications (student_id, job_id, status) VALUES (%s, %s, %s)",
            (student_id, job_id, "Applied"),
        )
        conn.commit()
        flash("Application submitted successfully.", "success")
    except Exception as exc:
        conn.rollback()
        flash(f"Could not apply: {exc}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("student_dashboard"))


@app.route("/company/register", methods=["GET", "POST"])
def company_register():
    if request.method == "POST":
        company_name = request.form["company_name"].strip()
        email = request.form["email"].strip()
        website = request.form["website"].strip()
        password = generate_password_hash(request.form["password"])

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO companies (company_name, email, website, password_hash)
                VALUES (%s, %s, %s, %s)
                """,
                (company_name, email, website, password),
            )
            conn.commit()
            flash("Company registration successful.", "success")
            return redirect(url_for("company_login"))
        except Exception as exc:
            conn.rollback()
            flash(f"Registration failed: {exc}", "error")
        finally:
            cur.close()
            conn.close()

    return render_template("company_register.html")


@app.route("/company/login", methods=["GET", "POST"])
def company_login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM companies WHERE email = %s", (email,))
        company = cur.fetchone()
        cur.close()
        conn.close()

        if company and check_password_hash(company["password_hash"], password):
            session["user_id"] = company["id"]
            session["name"] = company["company_name"]
            session["role"] = "company"
            flash("Welcome back!", "success")
            return redirect(url_for("company_dashboard"))

        flash("Invalid company credentials.", "error")

    return render_template("company_login.html")


@app.route("/company/dashboard")
@login_required("company")
def company_dashboard():
    company_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT id, title, location, package_lpa, created_at
        FROM jobs
        WHERE company_id = %s
        ORDER BY created_at DESC
        """,
        (company_id,),
    )
    jobs = cur.fetchall()

    cur.execute(
        """
        SELECT a.id, a.status, a.applied_at, s.name AS student_name, s.email,
               s.department, s.cgpa, j.title
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN jobs j ON a.job_id = j.id
        WHERE j.company_id = %s
        ORDER BY a.applied_at DESC
        """,
        (company_id,),
    )
    applicants = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("company_dashboard.html", jobs=jobs, applicants=applicants)


@app.route("/company/job/new", methods=["POST"])
@login_required("company")
def create_job():
    company_id = session["user_id"]
    title = request.form["title"].strip()
    description = request.form["description"].strip()
    location = request.form["location"].strip()
    package_lpa = request.form["package_lpa"].strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO jobs (company_id, title, description, location, package_lpa)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (company_id, title, description, location, package_lpa),
        )
        conn.commit()
        flash("Job posted successfully.", "success")
    except Exception as exc:
        conn.rollback()
        flash(f"Could not create job: {exc}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("company_dashboard"))


@app.route("/company/application/<int:application_id>/status", methods=["POST"])
@login_required("company")
def update_application_status(application_id):
    new_status = request.form["status"]
    allowed = {"Applied", "Shortlisted", "Rejected", "Selected"}

    if new_status not in allowed:
        flash("Invalid status.", "error")
        return redirect(url_for("company_dashboard"))

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE applications a
            JOIN jobs j ON a.job_id = j.id
            SET a.status = %s
            WHERE a.id = %s AND j.company_id = %s
            """,
            (new_status, application_id, session["user_id"]),
        )
        conn.commit()
        flash("Application status updated.", "success")
    except Exception as exc:
        conn.rollback()
        flash(f"Update failed: {exc}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("company_dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
