from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Task

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# In-memory store for tasks
tasks = []
next_task_id = 1

@app.post('/tasks', response_model=Task)
async def create_task(task: Task):
    global next_task_id
    task.id = next_task_id
    next_task_id += 1
    tasks.append(task)
    return task

@app.get('/tasks', response_model=list[Task])
async def get_tasks():
    return tasks

@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {'message': 'Task deleted successfully.'}