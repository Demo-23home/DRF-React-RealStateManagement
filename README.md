# 🏢 RealState Management Dashboard

A complete dashboard for managing a real estate community. This project is under active development, with new features continuously added. It provides a backend for property, profile, and issue management with a connected frontend for admins and tenants.

---

## 🚀 Project Overview

The RealState Management Dashboard allows users to:

- Manage apartment listings and tenants
- Create and track issues (maintenance, complaints)
- Handle posts and community interactions
- Manage user profiles, authentication, and ratings
- Send notifications via emails and tasks
- Generate reports and track activities
- Access a dashboard with real-time data and analytics

The backend is powered by Django REST Framework, Celery for async tasks, Redis for task queues, and PostgreSQL as the database. The frontend is a React/Next.js application inside the `client/` folder.

---

## 🧰 Tech Stack

- **Backend:** Django, Django REST Framework, Celery, Redis  
- **Frontend:** React / Next.js  
- **Database:** PostgreSQL  
- **Authentication:** Cookie-based / JWT via Djoser  
- **Containerization:** Docker & Docker Compose  
- **API Documentation:** Postman / Redoc  
- **Task Queues:** Celery & Flower  
- **Media Hosting:** Cloudinary  

---

## 🏗️ Architecture Overview

```
RealState/
├── client/           # React/Next.js frontend
├── core_apps/        # Django apps
│   ├── apartments/   # Apartment CRUDs
│   ├── common/       # Utilities, renderers, cookie auth
│   ├── issues/       # Issue tracking & notifications
│   ├── posts/        # Community posts
│   ├── profiles/     # User profiles & pipelines
│   ├── ratings/      # Ratings system
│   ├── reports/      # Reports & emails
│   └── users/        # Custom user model & auth
├── config/           # Django settings & URLs
├── docker/           # Docker configurations
├── media/            # Uploaded media files
├── staticfiles/      # Collected static files
├── manage.py
├── Makefile          # Development & deployment tasks
├── Pipfile
└── requirements/
```

Key Architectural Features:

- Modular Django apps for separation of concerns  
- Celery with Redis for asynchronous tasks  
- Cloudinary integration for media hosting  
- Postman API documentation for backend  
- Dockerized environment for consistent development & production  

---

## 🔐 Authentication & Authorization

- User registration and login via cookies / JWT  
- Protected endpoints for apartments, posts, issues, and ratings  
- Custom user model in `core_apps.users` with profile integration  
- Google OAuth support for external login  
- Role-based access control for admins vs tenants  

---

## 🏢 App Modules

### **Apartments**
- Create, update, delete, and list apartments  
- Assign tenants to apartments  
- Retrieve apartment details  

### **Profiles**
- Manage user profiles, avatars, and pipelines  
- Async profile tasks via Celery  

### **Issues**
- Create, track, and resolve maintenance or community issues  
- Email notifications on issue updates  
- Issue assignment to staff  

### **Posts**
- Community posts and comments  
- Filtering, permissions, and pagination  

### **Ratings**
- Tenants can rate technicians  
- Admin can view aggregated ratings  

### **Reports**
- Generate activity and issue reports  
- Send report emails to admins and users  

---

## 📖 API Documentation

Full API documentation is available via Postman:

🔗 [Postman API Docs](https://documenter.getpostman.com/view/29368996/2sAY4xAh3i)

---

## 🐳 Docker Setup

### Build services
```bash
make build
```

### Start development environment
```bash
make up
```

### Stop services
```bash
make down
```

### Rebuild without cache
```bash
make rebuild
```

---

## 🧪 Testing

- Unit tests for models, serializers, and views  
- Tests for apartments, profiles, issues, posts, and ratings  
- Run tests via Docker:

```bash
docker-compose run --rm app python manage.py test
```

---

## ⚙️ Development Workflow

- Apply migrations: `make migrate`  
- Create migrations: `make makemigrations`  
- Lint code: `make lint`  
- Open Django shell: `make django_shell`  

Frontend development:

- Run Next.js dev server in `client/` via Docker  
- Hot reload for real-time changes  

---

## 🔄 CI/CD Pipeline

- Dockerized builds for backend & frontend  
- Linting & automated tests on each commit  
- Ready for production deployment  

---

## 🔮 Future Improvements

- Full dashboard analytics  
- Notifications system for tenants & admins  
- Enhanced filtering & search for apartments and posts  
- Real-time updates using Django Channels or WebSockets  
- Expand Celery tasks for background processing  
- Integrate map views for apartment locations  

---

## 👨‍💻 Author

**Zeyad**  
Backend Developer | Python & Django  
