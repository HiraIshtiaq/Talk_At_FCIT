# FCIT_PROJECT - Quick Start Guide

## 📍 Project Location
**Path**: `C:\Users\User\.gemini\antigravity\scratch\FCIT_PROJECT`

## 🎯 What's Included

### Complete Django Backend
- ✅ 6 Django apps (Users, Discussions, Notifications, Reports, Search, Analytics)
- ✅ PostgreSQL database configuration
- ✅ Redis for WebSocket support
- ✅ JWT authentication with token blacklisting
- ✅ Swagger API documentation
- ✅ Docker deployment ready

### Key Features
1. **Email Validation**: Only @pucit.edu.pk emails allowed
2. **Role-Based Access**: User, Moderator, Admin
3. **Discussion System**: Posts, comments, categories, voting
4. **Real-Time Notifications**: WebSocket support via Django Channels
5. **Full-Text Search**: PostgreSQL search with ranking
6. **Content Moderation**: Reporting system with admin controls
7. **Analytics Dashboard**: Platform metrics for admins

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd C:\Users\User\.gemini\antigravity\scratch\FCIT_PROJECT\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
# Make sure PostgreSQL is running
# Create database: createdb fcit_db

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 3: Run Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/api/docs/ for Swagger documentation

## 🐳 Docker Alternative
```bash
cd C:\Users\User\.gemini\antigravity\scratch\FCIT_PROJECT
docker-compose up -d
```

## 📚 Documentation
- **README**: [backend/README.md](file:///C:/Users/User/.gemini/antigravity/scratch/FCIT_PROJECT/backend/README.md)
- **Walkthrough**: See artifacts panel for complete implementation details
- **API Docs**: http://localhost:8000/api/docs/ (after starting server)

## 🔑 Key API Endpoints

### Authentication
- `POST /api/auth/register/` - Register
- `POST /api/auth/login/` - Login (get JWT)
- `GET /api/auth/me/` - Profile

### Discussions
- `GET /api/discussions/posts/` - List posts
- `POST /api/discussions/posts/` - Create post
- `POST /api/discussions/posts/{id}/vote/` - Vote

### Notifications
- `GET /api/notifications/` - List notifications
- `WS /ws/notifications/` - WebSocket

### Admin
- `GET /api/analytics/` - Platform metrics
- `POST /api/analytics/users/{id}/suspend/` - Suspend user

## 📁 Project Structure
```
FCIT_PROJECT/
├── backend/
│   ├── apps/
│   │   ├── users/          # Auth & profiles
│   │   ├── discussions/    # Posts & comments
│   │   ├── notifications/  # Real-time alerts
│   │   ├── reports/        # Moderation
│   │   ├── search/         # Full-text search
│   │   └── analytics/      # Admin metrics
│   ├── config/             # Settings & URLs
│   ├── requirements.txt
│   └── manage.py
└── docker-compose.yml
```

## ✅ All Requirements Met
- [x] Django 4.2+ with PostgreSQL
- [x] JWT authentication
- [x] @pucit.edu.pk email validation
- [x] Discussion boards with categories
- [x] Comments and upvotes
- [x] Real-time notifications (WebSocket)
- [x] Full-text search
- [x] Admin moderation
- [x] Role-based permissions
- [x] API documentation (Swagger)
- [x] Docker deployment
- [x] Production-ready settings

## 🎓 Next Steps
1. Configure `.env` file with your database credentials
2. Run migrations and create superuser
3. Start the server and explore the API docs
4. Test authentication with @pucit.edu.pk email
5. Create categories and posts
6. Test WebSocket notifications

**Note**: The project is in the scratch directory. You mentioned wanting it on D drive - you can simply copy the entire `FCIT_PROJECT` folder to D:\ when ready.
