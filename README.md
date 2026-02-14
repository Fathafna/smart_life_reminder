# Smart Life Reminder System

A simple, elder-friendly web application for managing important life deadlines and receiving timely reminders.

## Project Structure

```
smart_life_reminder/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── database_setup.sql     # Database schema
├── .env                   # Environment variables
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    ├── js/
    │   └── main.js       # Main JavaScript
    └── images/           # Image assets
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database

```bash
# Open MySQL command line
mysql -u root -p

# Then run the SQL script
source database_setup.sql;
```

Or in MySQL Workbench, open and execute `database_setup.sql`.

### 3. Configure Environment Variables

Update `.env` file with your MySQL credentials if needed:

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=smart_reminder
```

### 4. Run the Application

```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

## Features

- ✅ User Registration & Login
- ✅ Add/Edit/Delete Tasks
- ✅ Set Reminder Preferences
- ✅ Task Status Management
- ✅ Elder-Friendly Interface
- 🔄 Daily Check-in Notifications (Coming Soon)
- 🔔 Scheduled Deadline Reminders (Coming Soon)

## Architecture Overview

### Frontend
- **HTML**: Semantic markup for accessibility
- **CSS**: Responsive design (mobile, tablet, desktop)
- **JavaScript**: Interactive features without external libraries

### Backend
- **Flask**: Lightweight Python web framework
- **MySQL**: Reliable relational database
- **Sessions**: Built-in Flask session management

### API Endpoints

#### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

#### Tasks
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

## Learning Path

### Phase 1: Foundation ✅
- [x] Project structure
- [x] Flask setup
- [x] Database schema
- [x] Authentication system

### Phase 2: Core Features
- [ ] Task management CRUD
- [ ] User dashboard
- [ ] Task status tracking

### Phase 3: Notifications
- [ ] Desktop notifications
- [ ] Scheduled reminders
- [ ] Daily check-in popup

### Phase 4: Polish & Deploy
- [ ] UI/UX improvements
- [ ] Testing
- [ ] Deployment

## Best Practices Implemented

- **Separation of Concerns**: Config, templates, static files separated
- **Security**: Password hashing, SQL parameterized queries
- **Responsiveness**: Mobile-first CSS approach
- **Error Handling**: Proper error pages and messages
- **Database Normalization**: Proper foreign keys and indexes
- **Code Organization**: Clear file structure

## Next Steps

1. Test the registration and login system
2. Verify database connection
3. Test task creation and management
4. Add notifications feature
5. Deploy to production

---

Built with ❤️ for helping people never miss important deadlines
