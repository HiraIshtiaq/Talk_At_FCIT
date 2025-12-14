# FCIT Backend - One-Click Setup Guide

## 🚀 Easiest Way to Run the Backend

Since Docker is not installed, I've created an **automated setup script** that does everything for you!

### Prerequisites

**Only Python is required!**

1. **Download Python**:
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11 or 3.12
   - **IMPORTANT**: During installation, check ✅ "Add Python to PATH"

### One-Click Setup & Run

1. **Double-click this file**:
   ```
   C:\Users\User\.gemini\antigravity\scratch\FCIT_PROJECT\SETUP_AND_RUN.bat
   ```

2. **The script will automatically**:
   - ✅ Check Python installation
   - ✅ Create virtual environment
   - ✅ Install all dependencies
   - ✅ Setup database (SQLite)
   - ✅ Run migrations
   - ✅ Ask you to create a superuser
   - ✅ Start the backend server

3. **When prompted for superuser**:
   - Email: `admin@pucit.edu.pk` (must end with @pucit.edu.pk)
   - First name: Your choice
   - Last name: Your choice
   - Password: Your choice

4. **Access your backend**:
   - 📚 API Docs: http://localhost:8000/api/docs/
   - 🔐 Admin: http://localhost:8000/admin/
   - 🌐 API: http://localhost:8000/api/

That's it! Everything is automated.

## What Database is Being Used?

The backend is configured to use **SQLite** (no PostgreSQL needed).

**SQLite Features**:
- ✅ No installation required
- ✅ Perfect for development and testing
- ✅ All features work except advanced PostgreSQL full-text search
- ✅ Simple text search is used instead

**To switch to PostgreSQL later**:
1. Install PostgreSQL
2. Follow instructions in `DEPLOYMENT_GUIDE.md`
3. Uncomment PostgreSQL config in `backend/config/settings.py`

## Stopping the Server

Press `Ctrl+C` in the terminal window where the server is running.

## Running Again

Just double-click `SETUP_AND_RUN.bat` again! It will:
- Skip steps that are already done
- Start the server immediately

## Troubleshooting

### "Python is not recognized"
**Solution**: 
1. Install Python from python.org
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Try again

### "pip install failed"
**Solution**:
1. Open PowerShell as Administrator
2. Run: `python -m pip install --upgrade pip`
3. Try the setup script again

### Port 8000 already in use
**Solution**:
1. Close any other programs using port 8000
2. Or edit `SETUP_AND_RUN.bat` and change `runserver` to `runserver 8001`
3. Access at http://localhost:8001/ instead

## What's Included?

✅ All backend features working:
- User authentication with @pucit.edu.pk validation
- JWT tokens
- Discussion boards
- Comments and voting
- Notifications
- Search
- Admin panel
- API documentation

## Next Steps After Setup

1. **Create categories** via admin panel:
   - Go to http://localhost:8000/admin/
   - Login with your superuser account
   - Add categories like "Guidance", "Assignments", etc.

2. **Test the API**:
   - Visit http://localhost:8000/api/docs/
   - Try registering a user
   - Login and get JWT tokens
   - Create posts and comments

3. **Explore features**:
   - Test voting system
   - Try search functionality
   - Check notifications
   - Review admin analytics

---

**The backend is complete and ready to use!** 🎉

No Docker, no PostgreSQL installation needed - just Python and one click!
