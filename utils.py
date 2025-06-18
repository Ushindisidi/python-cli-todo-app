import json
import os
from task import Task

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as file:
            data = json.load(file)
            return [Task(**item) for item in data]
    except json.JSONDecodeError:
        print("Error: Couldn't read tasks.json. Starting with an empty list.")
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=2)

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1

def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task.id == task_id:
            return task
    return None