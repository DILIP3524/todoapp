# 📝 To-Do List Web Application (Django)

A **To-Do List** web application with **RESTful APIs** and a **Bootstrap-based web interface**.  
Built using **Django** with **raw SQL queries** (no ORM) as per requirements.

---

## You can Read Documentation With Screenshot Directly in root Folder 

- file name:- Project_Document.pdf

---

## 🚀 Features
- Add, view, update, and delete tasks  
- RESTful API endpoints for CRUD operations  
- Bootstrap web interface for user-friendly interaction  
- Validations for required fields & correct date format (`YYYY-MM-DD`)  
- Default task status set to **Pending**  
- Separate apps for API and Web Interface  
- SQLite database for storage  

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/DILIP3524/todoapp.git
cd todoapp
```
### 2. Create Virtual Environment
```bash
python -m venv venv
# Activate
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate   
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Visit 👉 http://127.0.0.1:8000/

🔗 API Endpoints

Get All Tasks
```bash
GET /api/v1/all_tasks/
```
Create a Task
```bash
GET /api/v1/all_tasks/

# Request Body
# json
{
  "title": "Task",
  "description": "Details",
  "due_date": "2025-08-15"
}

```

Get Single Task
```bash
GET /api/v1/get_task/<pk>/
```
Update a Task
```bash
PUT /api/v1/get_task/<pk>/

# Request Body

# json

{
  "description": "Update task details",
  "status": "In Progress"
}
```

Delete a Task
```bash
DELETE /api/v1/get_task/<pk>/
```

🌐 Web Interface
👉 Navigate to: http://127.0.0.1:8000/

Available Features:

- Add tasks via a form

- View tasks in a table

- Update or delete tasks with one click

🛠️ Tech Stack
- Backend: Django 5, Python 3

- Database: SQLite

- Frontend: Bootstrap 5

- Testing: Django Test Client / Pytest

- Version Control: Git

✅ Testing
Run all tests

```bash
# run this command
pytest
```
Tests cover:

- Task creation with valid/invalid data

- Task retrieval

- Task update

- Task deletion

📂 Project Structure

```
todoapp/
│
├── api/                # REST API implementation
│   └── views.py
│
├── core/               # Web interface (Bootstrap templates)
│   └── views.py
│
├── templates/          # HTML templates
│   └── index.html
│
├── todoapp/            # Main Django project settings
│
├── db.sqlite3          # SQLite database
├── requirements.txt    # Dependencies
├── manage.py           # Django CLI
└── README.md           # Project Documentation

```

📌 Author

Dilip Kumar

📧 Email: dilipdev3524@gmail.com 

🐱‍💻 GitHub: @DILIP3524 

☕ Buy Me a Coffee: coff.ee/dilip3524


