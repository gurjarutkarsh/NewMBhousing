# 🏠 MB Housing — Inventory & CRM System

> Internal management platform for a real estate company — handling properties, customers, site visits, employee attendance, and weekly progress reporting.

---

## What is MB Housing?

MB Housing is a Django-based internal tool built for a real estate business to replace manual spreadsheets and disconnected workflows. It gives the team a single platform to manage apartment inventory, track customer interactions, schedule site visits, monitor employee attendance, and generate weekly progress reports — all with role-based access so each team member only sees what they need.

---

## Features

- 🏢 **Property & Apartment Inventory** — Manage projects, towers, and individual units with status tracking (available, booked, sold)
- 👥 **Customer Management (CRM)** — Maintain customer records, track leads, and manage the sales pipeline
- 📅 **Site Visit Scheduling** — Log and track customer site visits linked to specific properties and sales staff
- 🕐 **Employee Attendance** — Record and monitor daily staff attendance with progress tracking
- 📊 **Weekly Reports** — Auto-generate weekly progress summaries via `WeeklyReport.py`
- 🔐 **Role-Based Access Control** — Different permissions for admins, sales staff, and managers via customised Django Admin
- 🐳 **Docker Deployment** — Fully containerised with Docker + Gunicorn for production-ready deployment
- 🗄️ **PostgreSQL Database** — Relational data models optimised for real estate entities

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | PostgreSQL |
| Server | Gunicorn |
| Containerisation | Docker, Docker Compose |
| Frontend | JavaScript, HTML5, CSS3 |

---

## Project Structure

```
NewMBhousing/
├── MBInventoryTool/       # Main Django app (models, views, admin)
├── InventoryTool/         # Supporting inventory module
├── scripts/               # Utility scripts
├── staticfiles/           # Collected static assets
├── WeeklyReport.py        # Weekly progress report generator
├── manage.py              # Django management
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-container setup
├── gunicorn.conf.py       # Production server config
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variable template
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed ([get Docker](https://docs.docker.com/get-docker/))

### 1. Clone the repo

```bash
git clone https://github.com/gurjarutkarsh/NewMBhousing.git
cd NewMBhousing
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
SECRET_KEY=your_django_secret_key
DEBUG=False
DB_NAME=mbhousing
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

### 3. Build and run with Docker

```bash
docker compose up --build
```

### 4. Run migrations and create admin user

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

The app will be available at `http://localhost:8000`.

Log in at `http://localhost:8000/admin` with your superuser credentials.

### 5. Generate a weekly report

```bash
docker compose exec web python WeeklyReport.py
```

---

## Why This Project?

Most small real estate businesses in India run their operations on WhatsApp groups and Excel sheets — leading to missed follow-ups, lost customer data, and no visibility into team performance. MB Housing was built to solve exactly that: a centralised, role-aware internal tool that gives management real-time oversight while keeping the workflow simple for field staff.

---

## Author

**Utkarsh Gurjar**
[LinkedIn](https://www.linkedin.com/in/utkarsh-gurjar-7a92591b4/) · [GitHub](https://github.com/gurjarutkarsh)