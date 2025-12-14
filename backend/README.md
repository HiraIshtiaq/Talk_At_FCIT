# Talk@FCIT Backend

Complete Django backend for the FCIT academic discussion platform.

## Features

- ✅ JWT Authentication with email verification
- ✅ @pucit.edu.pk email domain restriction
- ✅ Discussion boards with categories
- ✅ Comments and nested replies
- ✅ Upvote/downvote system
- ✅ Real-time notifications (WebSocket)
- ✅ PostgreSQL full-text search
- ✅ Content reporting & moderation
- ✅ Admin analytics dashboard
- ✅ Role-based permissions (User/Moderator/Admin)

## Tech Stack

- **Framework**: Django 4.2+
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Real-time**: Django Channels + Redis
- **Authentication**: JWT (Simple JWT)

## Project Structure

```
backend/
├── config/              # Django settings, URLs, ASGI/WSGI
├── apps/
│   ├── users/          # Authentication & user management
│   ├── discussions/    # Posts, comments, categories, votes
│   ├── notifications/  # Real-time notifications
│   ├── reports/        # Content reporting
│   ├── search/         # Full-text search
│   └── analytics/      # Admin metrics
├── requirements.txt
└── manage.py
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis 5+

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Update database credentials and other settings

4. **Setup database**:
   ```bash
   # Create PostgreSQL database
   createdb fcit_db
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   # HTTP server
   python manage.py runserver
   
   # WebSocket server (in another terminal)
   daphne -b 0.0.0.0 -p 8001 config.asgi:application
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/logout/` - Logout (blacklist token)
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/me/` - Update profile

### Discussions
- `GET /api/discussions/posts/` - List posts
- `POST /api/discussions/posts/` - Create post
- `GET /api/discussions/posts/{id}/` - Get post details
- `POST /api/discussions/posts/{id}/vote/` - Vote on post
- `GET /api/discussions/posts/{id}/comments/` - List comments
- `POST /api/discussions/posts/{id}/comments/` - Create comment

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/{id}/read/` - Mark as read
- `WS /ws/notifications/` - WebSocket connection

### Search
- `GET /api/search/posts/?q=keyword` - Search posts

### Admin/Analytics
- `GET /api/analytics/` - Platform analytics
- `GET /api/analytics/users/` - User list
- `POST /api/analytics/users/{id}/suspend/` - Suspend user

## Testing

Run tests:
```bash
python manage.py test
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL and Redis
4. Collect static files: `python manage.py collectstatic`
5. Use Gunicorn + Daphne for serving
6. Set up Nginx as reverse proxy

## License

MIT
