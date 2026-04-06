from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from todo_logic import db, User, Task
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mlue-manager-secret-dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mlue_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database on startup
with app.app_context():
    db.create_all()

# Helper to provide common context
def get_categories_priorities():
    return ['School', 'Work', 'Personal', 'Other'], ['High', 'Medium', 'Low']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    search = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    priority_filter = request.args.get('priority', '')
    
    query = Task.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(Task.name.ilike(f"%{search}%"))
    if category_filter:
        query = query.filter_by(category=category_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    
    tasks = query.all()
    filtered_tasks = [(t.id, t.to_dict()) for t in tasks]
    
    categories, priorities = get_categories_priorities()
    
    return render_template('index.html', 
                         filtered_tasks=filtered_tasks, 
                         all_tasks=[t.to_dict() for t in current_user.tasks],
                         categories=categories,
                         priorities=priorities,
                         search=search,
                         category_filter=category_filter,
                         priority_filter=priority_filter,
                         user=current_user)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    task_text = request.form.get('task')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date', '')
    category = request.form.get('category', 'Other')
    
    new_task = Task(
        name=task_text,
        priority=priority,
        due_date=due_date,
        category=category,
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('task_item.html', task_id=new_task.id, task=new_task.to_dict())
        return jsonify({'success': True, 'html': html})
        
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'success': False}), 403
    db.session.delete(task)
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
        
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'success': False}), 403
    task.done = not task.done
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'done': task.done})
        
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        task.name = request.form.get('task')
        task.priority = request.form.get('priority')
        task.due_date = request.form.get('due_date')
        task.category = request.form.get('category')
        db.session.commit()
        return redirect(url_for('index'))
    
    categories, priorities = get_categories_priorities()
    return render_template('edit.html', 
                         task_id=task_id, 
                         task=task.to_dict(),
                         categories=categories,
                         priorities=priorities,
                         user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
