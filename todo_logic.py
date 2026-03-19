# ToDo Logic for Task Management

class Task:
    def __init__(self, name, priority, due_date, category):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.category = category

    def __repr__(self):
        return f"Task(name={self.name}, priority={self.priority}, due_date={self.due_date}, category={self.category})"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, priority, due_date, category):
        task = Task(name, priority, due_date, category)
        self.tasks.append(task)
        return task

    def remove_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def update_priority(self, task_name, new_priority):
        for task in self.tasks:
            if task.name == task_name:
                task.priority = new_priority
                break

    def set_due_date(self, task_name, new_due_date):
        for task in self.tasks:
            if task.name == task_name:
                task.due_date = new_due_date
                break

    def categorize_task(self, task_name, new_category):
        for task in self.tasks:
            if task.name == task_name:
                task.category = new_category
                break

    def __repr__(self):
        return f"TaskManager(tasks={self.tasks})"

# Example Usage
# manager = TaskManager()
# manager.add_task('Buy groceries', 1, '2026-03-20', 'Shopping')
# print(manager)