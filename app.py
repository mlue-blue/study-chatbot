from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# Load tasks from file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=2)

# Routes
@app.route('/')
def index():
    tasks = load_tasks()
    search = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    priority_filter = request.args.get('priority', '')
    
    # Filter tasks
    filtered_tasks = []
    for i, task in enumerate(tasks):
        # Search filter
        if search and search not in task['task'].lower():
            continue
        # Category filter
        if category_filter and task.get('category', '') != category_filter:
            continue
        # Priority filter
        if priority_filter and task.get('priority', 'Medium') != priority_filter:
            continue
        filtered_tasks.append((i, task))
    
    categories = ['School', 'Work', 'Personal', 'Other']
    priorities = ['High', 'Medium', 'Low']
    
    return render_template('index.html', 
                         tasks=filtered_tasks, 
                         all_tasks=tasks,
                         categories=categories,
                         priorities=priorities,
                         search=search,
                         category_filter=category_filter,
                         priority_filter=priority_filter)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    task_text = request.form.get('task')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date', '')
    category = request.form.get('category', 'Other')
    
    if task_text:
        tasks.append({
            'task': task_text,
            'done': False,
            'priority': priority,
            'due_date': due_date,
            'category': category
        })
        save_tasks(tasks)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = load_tasks()
    
    if request.method == 'POST':
        if 0 <= task_id < len(tasks):
            tasks[task_id]['task'] = request.form.get('task', tasks[task_id]['task'])
            tasks[task_id]['priority'] = request.form.get('priority', tasks[task_id].get('priority', 'Medium'))
            tasks[task_id]['due_date'] = request.form.get('due_date', tasks[task_id].get('due_date', ''))
            tasks[task_id]['category'] = request.form.get('category', tasks[task_id].get('category', 'Other'))
            save_tasks(tasks)
            return redirect(url_for('index'))
    
    if 0 <= task_id < len(tasks):
        task = tasks[task_id]
        categories = ['School', 'Work', 'Personal', 'Other']
        priorities = ['High', 'Medium', 'Low']
        return render_template('edit.html', 
                             task_id=task_id, 
                             task=task,
                             categories=categories,
                             priorities=priorities)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
