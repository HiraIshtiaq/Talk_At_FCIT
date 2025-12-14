# 🚀 How to Run Talk@FCIT

Follow these steps to start the full-stack application (Backend + Frontend).

## 1. Prerequisites
- **Docker Desktop** must be installed and running.
- **Node.js** (v18+) must be installed.

## 2. Start the Backend (API & Database)
Open a terminal in the project root (`FCIT_PROJECT/`) and run:
```bash
docker-compose up -d
```
> This starts Django (Port 8000), PostgreSQL (DB), and Redis.

**Verify Backend:**
- Go to [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) to see the API documentation.
- If it loads, the backend is running successfully.

## 3. Start the Frontend (React App)
Open a **new key** terminal window, navigate to the `frontend` folder, and start the server:
```bash
cd frontend
npm run dev
```
> The app will run at [http://localhost:5173/](http://localhost:5173/)

## 4. Login Credentials
Use the System Administrator account to log in:

- **Email**: `shayan@pucit.edu.pk`
- **Password**: `emaan@123`

---

## 🛠️ Common Commands

### Stop the Backend
```bash
docker-compose down
```

### Create a Superuser (Manually)
If you need to create another admin:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Reset Database (Fresh Start)
```bash
docker-compose down -v
docker-compose up -d --build
```
