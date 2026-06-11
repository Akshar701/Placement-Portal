# DBMS Project Plan  
## Title
**College Placement Portal**

## 1) Project Overview
The College Placement Portal is a database-driven web application that manages the campus recruitment process between students and companies.  
It supports student and company registration, secure login, job posting, application submission, and recruitment status tracking.

This project demonstrates practical DBMS concepts such as:
- Relational schema design
- Entity relationships and foreign keys
- Data integrity via constraints
- Transaction handling with commit/rollback
- SQL-based reporting for dashboards

## 2) Problem Statement
Manual placement processes are time-consuming and error-prone when managing student profiles, company openings, and application statuses.  
A centralized system is required to:
- Maintain accurate placement records
- Prevent duplicate applications
- Provide role-specific dashboards
- Ensure data consistency and faster communication

## 3) Objectives
- Build a normalized relational database for placement management.
- Implement secure role-based access for students and companies.
- Enable end-to-end workflow from job posting to final selection.
- Enforce constraints to avoid duplicate or inconsistent records.
- Provide real-time status visibility to both stakeholders.

## 4) Scope
### In Scope
- Student registration/login
- Company registration/login
- Job creation by companies
- Job applications by students
- Status updates by companies (`Applied`, `Shortlisted`, `Rejected`, `Selected`)
- Role-based dashboards

### Out of Scope (Current Version)
- Admin panel for placement cell
- Resume file upload and parsing
- Interview scheduling and notifications
- Advanced analytics and reports export
- Multi-college or multi-campus support

## 5) Technology Stack
- **Backend:** Python (Flask)
- **Database:** MySQL
- **Frontend:** HTML, CSS, Jinja templates
- **DB Access Layer:** `mysql-connector-python` with connection pooling
- **Security:** Password hashing (`werkzeug.security`)
- **Environment Config:** `.env` via `python-dotenv`

## 6) System Modules
1. **Authentication Module**
   - Student register/login
   - Company register/login
   - Session-based access control by role

2. **Student Module**
   - Browse latest jobs
   - Apply to jobs
   - Track own application status

3. **Company Module**
   - Post new jobs
   - View all applicants for posted jobs
   - Update application status

4. **Data Management Module**
   - Relational table storage
   - Foreign key-based relationships
   - Constraint checks and transaction safety

## 7) Database Design
### Core Entities
- `students`
- `companies`
- `jobs`
- `applications`

### Table-wise Schema Summary
1. **students**
   - `id` (PK)
   - `name`, `email (UNIQUE)`, `phone`, `department`, `cgpa`
   - `password_hash`
   - `created_at`

2. **companies**
   - `id` (PK)
   - `company_name`, `email (UNIQUE)`, `website`
   - `password_hash`
   - `created_at`

3. **jobs**
   - `id` (PK)
   - `company_id` (FK -> `companies.id`)
   - `title`, `description`, `location`, `package_lpa`
   - `created_at`

4. **applications**
   - `id` (PK)
   - `student_id` (FK -> `students.id`)
   - `job_id` (FK -> `jobs.id`)
   - `status` ENUM
   - `applied_at`
   - `UNIQUE(student_id, job_id)` to prevent duplicate applications

### Relationships
- One company can post many jobs (1:N).
- One student can apply to many jobs (1:N through applications).
- One job can have many applications (1:N).
- `applications` acts as a bridge table for student-job many-to-many relation.

### Constraints Used
- Primary keys on all tables
- Unique constraints on user emails
- Unique composite key on student-job pair
- Foreign key constraints with `ON DELETE CASCADE` and `ON UPDATE CASCADE`
- ENUM constraint for valid application statuses

## 8) Normalization
- **1NF:** Atomic fields and no repeating groups.
- **2NF:** Non-key attributes fully depend on full primary key.
- **3NF:** No transitive dependency among non-key attributes.

The schema avoids redundancy and improves update consistency.

## 9) Functional Workflow
1. Student/Company registers and credentials are stored securely.
2. User logs in; session stores role and user identity.
3. Company posts jobs.
4. Student dashboard lists jobs and checks whether already applied.
5. Student applies; duplicate applications blocked by app logic + DB constraint.
6. Company reviews applicants and updates status.
7. Student tracks final status from dashboard.

## 10) Important SQL Operations Demonstrated
- `INSERT` for registrations, jobs, and applications
- `SELECT` with `JOIN` for dashboards
- `UPDATE` with join for status change authorization
- `EXISTS` subquery to check applied/not-applied
- `ORDER BY` for recent activity
- Constraint-driven integrity enforcement

## 11) Security and Integrity Measures
- Passwords are stored as hashes, not plain text.
- Session-based role check protects sensitive routes.
- Server-side validation for allowed application statuses.
- Transactions with rollback on failure.
- Parameterized SQL queries to reduce injection risk.

## 12) Project Directory Structure
- `app.py` - Flask routes and business logic
- `db.py` - MySQL connection pool and DB config
- `schema.sql` - Database schema
- `templates/` - UI templates
- `static/` - CSS assets
- `requirements.txt` - Python dependencies
- `.env` - Runtime configuration

## 13) Setup and Execution Plan
1. Create and activate virtual environment.
2. Install dependencies from `requirements.txt`.
3. Configure `.env` with MySQL credentials and database name.
4. Run SQL schema to create tables.
5. Start Flask app and verify role-based workflows.

## 14) Testing Plan
### Functional Test Cases
- Student can register and log in.
- Company can register and log in.
- Company can post a new job.
- Student can apply exactly once per job.
- Company can update status only for its own job applications.
- Dashboards correctly display joined data.

### Integrity Test Cases
- Duplicate email should fail.
- Duplicate student-job application should fail.
- Invalid status value should be rejected.
- Deleting a company should cascade delete its jobs and applications.

## 15) Deliverables
- Source code (Flask app + templates + static files)
- SQL schema file
- Setup instructions
- This project plan/report document

## 16) Limitations
- No separate admin approval workflow.
- Minimal input validation rules for domain constraints.
- No document upload/storage support.
- No email/SMS notification pipeline.

## 17) Future Enhancements
- Add placement officer/admin dashboard.
- Add resume upload and skill-based filtering.
- Add interview scheduling and calendar integration.
- Add analytics (placement rate, average package, department-wise stats).
- Add REST API layer and JWT for scalable clients.

## 18) Conclusion
The College Placement Portal successfully models a real-world placement workflow using core DBMS principles.  
It provides a clean and practical implementation of relational design, constraints, joins, and transactional operations while supporting role-based user experiences.

---
## Optional Submission Details (Fill Before Final Submission)
- **Student Name:**  
- **Roll Number:**  
- **Department/Semester:**  
- **Guide/Faculty Name:**  
- **Institute Name:**  
- **Submission Date:**  

