# College Placement Portal (DBMS Mini Project)

A Flask + MySQL based placement portal for college use.

## Features
- Student registration and login
- Company registration and login
- Company can post jobs
- Students can apply to jobs
- Company can update application status (Applied, Shortlisted, Rejected, Selected)
- Dashboard for both student and company

## Tech Stack
- Python (Flask)
- MySQL
- HTML/CSS (Jinja templates)

## Project Structure
- app.py - Flask application routes and logic
- db.py - MySQL connection pool setup
- schema.sql - Database schema for the project
- templates/ - HTML templates
- static/style.css - Stylesheet
- .env.example - Environment variable template

## Setup Instructions
1. Create and activate virtual environment
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables
   - Copy `.env.example` to `.env`
   - Update MySQL username/password/database values

4. Create database and tables
   ```bash
   mysql -u root -p < schema.sql
   ```

5. Run application
   ```bash
   python app.py
   ```

6. Open browser
   - http://127.0.0.1:5000

## Notes for Viva/Report
- Demonstrates DBMS concepts: entities, relationships, constraints, and CRUD operations.
- Uses foreign keys and unique constraints to maintain data integrity.
- Supports role-based workflows (student/company).
