from flask import Flask, render_template, request, redirect, url_for, jsonify
from todo_logic import TaskManager

app = Flask(__name__)
manager = TaskManager('tasks.json')

# Helper to provide common context
def get_categories_priorities():
    return ['School', 'Work', 'Personal', 'Other'], ['High', 'Medium', 'Low']

@app.route('/')
def index():
    search = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    priority_filter = request.args.get('priority', '')
    
    filtered_tasks = manager.get_filtered_tasks(
        search=search, 
        category=category_filter, 
        priority=priority_filter
    )
    
    categories, priorities = get_categories_priorities()
    
    return render_template('index.html', 
                         filtered_tasks=filtered_tasks, 
                         all_tasks=manager.get_all_dicts(),
                         categories=categories,
                         priorities=priorities,
                         search=search,
                         category_filter=category_filter,
                         priority_filter=priority_filter)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date', '')
    category = request.form.get('category', 'Other')
    
    manager.add_task(task_text, priority, due_date, category)
    
    # Handle AJAX Request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        task_id = len(manager.tasks) - 1
        html = render_template('task_item.html', task_id=task_id, task=manager.tasks[task_id].to_dict())
        return jsonify({'success': True, 'html': html})
        
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    manager.delete_task(task_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
        
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = manager.toggle_task(task_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'done': task.done if task else False})
        
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        manager.update_task(
            task_id,
            name=request.form.get('task'),
            priority=request.form.get('priority'),
            due_date=request.form.get('due_date'),
            category=request.form.get('category')
        )
        return redirect(url_for('index'))
    
    # GET request: load the task to edit
    all_tasks = manager.tasks
    if 0 <= task_id < len(all_tasks):
        task = all_tasks[task_id].to_dict()
        categories, priorities = get_categories_priorities()
        return render_template('edit.html', 
                             task_id=task_id, 
                             task=task,
                             categories=categories,
                             priorities=priorities)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
