import json
import os
from datetime import datetime, date
from task import Task

TASKS_FILE = "tasks.json"

def load_tasks():
    # Create file if doesn't exist
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
    
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            if not isinstance(tasks_data, list):
                print(f"Warning: {TASKS_FILE} contains invalid data format.Resetting tasks.")
                return []
            return [
                Task(
                    t['id'],
                    t['title'],
                    t['description'],
                    t.get('due_date'),
                    t.get('completed', False)
                ) for t in tasks_data
            ]
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {TASKS_FILE}. File might be corrupt and empty.")
        return []
    except IOError as e:
        print(f"Error reading {TASKS_FILE}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading tasks: {e}")
        return []

def save_tasks(tasks):
    """
    Save a list of Task objects to the tasks file.

    Args:
        tasks (list[Task]): A list of Task objects to save.
    """
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4)
    except IOError as e:
        print(f"Error writing to {TASKS_FILE}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving tasks: {e}")

def generate_new_id(tasks):
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1

def validate_date(date_str):
    if not date_str:
        return None
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return None
def is_due_today(task):
        if not task.due_date:
            return False
        try:
            due_date_obj = datetime.strptime(task.due_date, "%Y-%m-%d").date()
            return due_date_obj == date.today()
        except ValueError:
            return False