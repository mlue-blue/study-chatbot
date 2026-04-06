import json
import os

class Task:
    def __init__(self, name, priority='Medium', due_date='', category='Other', done=False):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.done = done

    def to_dict(self):
        return {
            'task': self.name,
            'priority': self.priority,
            'due_date': self.due_date,
            'category': self.category,
            'done': self.done
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('task', ''),
            priority=data.get('priority', 'Medium'),
            due_date=data.get('due_date', ''),
            category=data.get('category', 'Other'),
            done=data.get('done', False)
        )

    def __repr__(self):
        return f"Task(name={self.name}, priority={self.priority}, done={self.done})"


class TaskManager:
    def __init__(self, storage_file='tasks.json'):
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.storage_file):
            return []
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(t) for t in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_tasks(self):
        with open(self.storage_file, 'w') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add_task(self, name, priority='Medium', due_date='', category='Other'):
        if not name:
            return None
        task = Task(name, priority, due_date, category)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()
            return removed
        return None

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = not self.tasks[index].done
            self.save_tasks()
            return self.tasks[index]
        return None

    def update_task(self, index, name=None, priority=None, due_date=None, category=None):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            if name is not None: task.name = name
            if priority is not None: task.priority = priority
            if due_date is not None: task.due_date = due_date
            if category is not None: task.category = category
            self.save_tasks()
            return task
        return None

    def get_filtered_tasks(self, search='', category='', priority=''):
        filtered = []
        for i, task in enumerate(self.tasks):
            if search and search.lower() not in task.name.lower():
                continue
            if category and task.category != category:
                continue
            if priority and task.priority != priority:
                continue
            filtered.append((i, task.to_dict()))
        return filtered

    def get_all_dicts(self):
        return [t.to_dict() for t in self.tasks]
