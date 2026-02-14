from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import hashlib
import functools
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Task(db.Model):
    """Task model"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    reminder_days = db.Column(db.String(100), default='7')  # Store as comma-separated string like "1,7,14"
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='pending')  # pending, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.strftime('%Y-%m-%d'),
            'reminder_days': self.reminder_days,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Reminder(db.Model):
    """Reminder model"""
    __tablename__ = 'reminders'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== HELPER FUNCTIONS ====================

def login_required(f):
    """Decorator to require login"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not all([email, password, name]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        try:
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                return jsonify({'success': False, 'message': 'Email already registered'}), 400
            
            # Create new user
            hashed_password = hash_password(password)
            new_user = User(name=name, email=email, password=hashed_password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Registration successful. Please login.'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        try:
            hashed_password = hash_password(password)
            user = User.query.filter_by(email=email, password=hashed_password).first()
            
            if user:
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_email'] = user.email
                return jsonify({'success': True, 'message': 'Login successful'}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

@app.route('/api/reminders', methods=['GET'])
@login_required
def get_reminders():
    """Get tasks that should trigger reminders today"""
    try:
        from datetime import date, timedelta
        today = date.today()
        
        # Get all pending tasks
        tasks = Task.query.filter_by(
            user_id=session['user_id'],
            status='pending'
        ).all()
        
        reminders_to_show = []
        
        for task in tasks:
            days_until_due = (task.due_date - today).days
            
            # Parse reminder_days (could be "1,7,14" or include "daily")
            reminder_string = str(task.reminder_days)
            reminder_parts = [x.strip() for x in reminder_string.split(',')]
            has_daily = 'daily' in reminder_parts
            
            # Extract numeric reminders
            reminder_days_list = []
            for part in reminder_parts:
                try:
                    reminder_days_list.append(int(part))
                except:
                    pass  # Skip non-numeric values like "daily"
            
            # Check if task should trigger a reminder
            # 1. If due today or overdue
            if days_until_due <= 0:
                urgency = 'critical' if days_until_due == 0 else 'critical'
                message = f"⚠️ {task.title} is due TODAY!" if days_until_due == 0 else f"🔴 {task.title} is OVERDUE by {abs(days_until_due)} days!"
                reminders_to_show.append({
                    'id': task.id,
                    'title': task.title,
                    'message': message,
                    'urgency': urgency,
                    'days_left': days_until_due
                })
            # 2. If due tomorrow
            elif days_until_due == 1:
                reminders_to_show.append({
                    'id': task.id,
                    'title': task.title,
                    'message': f"⚠️ {task.title} is due TOMORROW!",
                    'urgency': 'high',
                    'days_left': 1
                })
            # 3. If daily reminder is enabled (show reminder every day until due date)
            elif has_daily and days_until_due > 1:
                reminders_to_show.append({
                    'id': task.id,
                    'title': task.title,
                    'message': f"📅 {task.title} - Due in {days_until_due} days",
                    'urgency': 'medium',
                    'days_left': days_until_due
                })
            # 4. If due on any of the specific reminder_days
            elif days_until_due in reminder_days_list:
                reminders_to_show.append({
                    'id': task.id,
                    'title': task.title,
                    'message': f"{task.title} - Due in {days_until_due} days",
                    'urgency': 'medium',
                    'days_left': days_until_due
                })
        
        return jsonify({'success': True, 'reminders': reminders_to_show}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/daily-checkin', methods=['GET'])
@login_required
def daily_checkin():
    """Get the daily check-in notification"""
    return jsonify({
        'success': True,
        'message': "👋 Heyy! Do you have anything important to add today?",
        'icon': '📝'
    }), 200

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get all tasks for logged-in user"""
    try:
        tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.due_date.asc()).all()
        return jsonify({'success': True, 'tasks': [task.to_dict() for task in tasks]}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    """Add a new task"""
    from datetime import date
    data = request.get_json()
    title = data.get('title')
    due_date = data.get('due_date')  # Format: YYYY-MM-DD
    reminder_days = data.get('reminder_days', '7')  # Can be comma-separated like "1,7,14"
    priority = data.get('priority', 'medium')
    
    if not all([title, due_date]):
        return jsonify({'success': False, 'message': 'Title and due date required'}), 400
    
    try:
        new_task = Task(
            user_id=session['user_id'],
            title=title,
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date(),
            reminder_days=reminder_days,  # Store as comma-separated string
            priority=priority
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        # Check if this task should trigger immediate reminders
        reminders = []
        today = date.today()
        days_until_due = (new_task.due_date - today).days
        
        # Parse reminder_days (could be "1,7,14" or include "daily")
        reminder_string = str(reminder_days)
        reminder_parts = [x.strip() for x in reminder_string.split(',')]
        has_daily = 'daily' in reminder_parts
        
        # Extract numeric reminders
        reminder_days_list = []
        for part in reminder_parts:
            try:
                reminder_days_list.append(int(part))
            except:
                pass  # Skip non-numeric values like "daily"
        
        # Check if task should trigger immediate reminders
        if days_until_due == 0:
            reminders.append({
                'id': new_task.id,
                'title': new_task.title,
                'message': f"⚠️ {new_task.title} is due TODAY!",
                'urgency': 'critical',
                'days_left': 0
            })
        elif days_until_due == 1:
            reminders.append({
                'id': new_task.id,
                'title': new_task.title,
                'message': f"⚠️ {new_task.title} is due TOMORROW!",
                'urgency': 'high',
                'days_left': 1
            })
        elif has_daily and days_until_due > 1:
            reminders.append({
                'id': new_task.id,
                'title': new_task.title,
                'message': f"📅 {new_task.title} - Due in {days_until_due} days",
                'urgency': 'medium',
                'days_left': days_until_due
            })
        else:
            # Check each specific reminder day
            for reminder_day in reminder_days_list:
                if days_until_due == reminder_day:
                    reminders.append({
                        'id': new_task.id,
                        'title': new_task.title,
                        'message': f"{new_task.title} - Due in {days_until_due} days",
                        'urgency': 'medium',
                        'days_left': days_until_due
                    })
                    break
        
        return jsonify({
            'success': True, 
            'message': 'Task added', 
            'task_id': new_task.id,
            'reminders': reminders  # Return array of reminders
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update a task"""
    data = request.get_json()
    
    try:
        task = Task.query.get(task_id)
        
        if not task or task.user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Update fields
        if 'status' in data:
            task.status = data['status']
        if 'title' in data:
            task.title = data['title']
        if 'due_date' in data:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        if 'priority' in data:
            task.priority = data['priority']
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Task updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get(task_id)
        
        if not task or task.user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Task deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ==================== DATABASE INITIALIZATION ====================

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
