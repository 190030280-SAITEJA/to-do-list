from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Task Model with due_date
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    due_date = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials, try again!", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "warning")
            return redirect(url_for('signup'))
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    filter_status = request.args.get('status', 'All')
    query = Task.query.filter_by(user_id=session['user_id'])

    if filter_status != 'All':
        query = query.filter_by(status=filter_status)

    tasks = query.all()

    today = datetime.today().date()
    for task in tasks:
        if task.due_date:
            try:
                task.is_overdue = datetime.strptime(task.due_date, '%Y-%m-%d').date() < today
            except ValueError:
                task.is_overdue = False
        else:
            task.is_overdue = False

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        priority = request.form['priority']
        due_date = request.form.get('due_date')
        new_task = Task(title=title, category=category, priority=priority, due_date=due_date, user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', tasks=tasks, filter_status=filter_status)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        priority = request.form['priority']
        due_date = request.form.get('due_date')
        new_task = Task(title=title, category=category, priority=priority, due_date=due_date, user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if 'user_id' not in session or task.user_id != session['user_id']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.category = request.form['category']
        task.priority = request.form['priority']
        task.status = request.form['status']
        task.due_date = request.form.get('due_date')
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if 'user_id' not in session or task.user_id != session['user_id']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "danger")
    return redirect(url_for('dashboard'))

@app.route('/toggle_status/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    if 'user_id' not in session or task.user_id != session['user_id']:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))

    task.status = 'Completed' if task.status != 'Completed' else 'Pending'
    db.session.commit()
    flash("Task status updated!", "info")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
