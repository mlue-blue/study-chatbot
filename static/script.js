// Script for enhanced to-do app with smooth animations

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Advanced To-Do App Loaded!');

    const taskList = document.querySelector('.task-list');
    const addTaskForm = document.querySelector('.add-task-form');
    const taskInput = document.querySelector('.task-input');

    // Handle AJAX Task Addition
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/add', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Create temporary container to parse HTML string
                    const temp = document.createElement('div');
                    temp.innerHTML = data.html;
                    const newTask = temp.firstElementChild;
                    
                    // Add to list
                    if (taskList) {
                        taskList.appendChild(newTask);
                    } else {
                        // If no tasks existed, we might need to refresh or create the UL
                        location.reload();
                    }
                    
                    // Reset form
                    taskInput.value = '';
                    taskInput.style.height = 'auto';
                    
                    // Remove animation class after it finishes to allow hover transitions
                    setTimeout(() => {
                        newTask.classList.remove('new-task-animation');
                    }, 600);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Delegation for Task Actions (Complete/Delete)
    if (taskList) {
        taskList.addEventListener('click', function(e) {
            // Handle Completion Toggle
            if (e.target.classList.contains('task-checkbox')) {
                e.preventDefault();
                const checkbox = e.target;
                const taskItem = checkbox.closest('.task-item');
                const taskId = taskItem.getAttribute('data-id');
                
                fetch(`/complete/${taskId}`, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        checkbox.checked = data.done;
                        if (data.done) {
                            taskItem.classList.add('completed');
                            taskItem.style.transform = 'scale(0.98)';
                            setTimeout(() => taskItem.style.transform = '', 200);
                        } else {
                            taskItem.classList.remove('completed');
                        }
                    }
                });
            }

            // Handle Deletion with Animation
            if (e.target.classList.contains('btn-delete')) {
                e.preventDefault();
                if (!confirm('Delete this task?')) return;

                const btn = e.target;
                const taskItem = btn.closest('.task-item');
                const taskId = taskItem.getAttribute('data-id');

                fetch(`/delete/${taskId}`, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Charming exit animation
                        taskItem.style.transform = 'translateX(100px) scale(0.5)';
                        taskItem.style.opacity = '0';
                        setTimeout(() => {
                            taskItem.remove();
                            if (taskList.children.length === 0) {
                                location.reload(); // Show "No tasks" message
                            }
                        }, 400);
                    }
                });
            }
        });
    }

    // Auto-submit filter form on select change
    document.querySelectorAll('.filter-select').forEach(select => {
        select.addEventListener('change', function() {
            this.closest('.filter-form').submit();
        });
    });

    // Expand textarea on input
    if (taskInput) {
        taskInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});
