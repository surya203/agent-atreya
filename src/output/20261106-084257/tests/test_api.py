import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Tests for the /tasks endpoint

def test_create_task():
    response = client.post('/tasks', json={'title': 'Test Task', 'completed': False})
    assert response.status_code == 200
    assert response.json()['title'] == 'Test Task'
    assert 'id' in response.json()


def test_get_tasks():
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_task():
    # First, create a task
    response = client.post('/tasks', json={'title': 'Task to Delete', 'completed': False})
    task_id = response.json()['id']
    # Now delete the task
    delete_response = client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 200
    assert delete_response.json()['message'] == 'Task deleted successfully.'
    # Verify it's deleted
    get_response = client.get('/tasks')
    assert task_id not in [task['id'] for task in get_response.json()]  # Ensure the deleted task is not in the list
