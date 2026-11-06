const taskForm = document.getElementById('taskForm');
const taskList = document.getElementById('taskList');

// Fetch tasks from the server and display them
async function fetchTasks() {
    const response = await fetch('http://127.0.0.1:8000/tasks');
    const tasks = await response.json();
    taskList.innerHTML = '';
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerText = task.title;
        li.setAttribute('data-id', task.id);
        li.innerHTML += ' <button class="delete-btn">Delete</button>';
        taskList.appendChild(li);
    });
}

// Add a new task
taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const taskTitle = document.getElementById('taskTitle').value;
    const response = await fetch('http://127.0.0.1:8000/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: taskTitle, completed: false })
    });
    const task = await response.json();
    fetchTasks();
    taskForm.reset();
});

// Delete a task
taskList.addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-btn')) {
        const taskId = e.target.parentElement.getAttribute('data-id');
        await fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
            method: 'DELETE'
        });
        fetchTasks();
    }
});

// Initial fetch of tasks
fetchTasks();
