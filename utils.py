import json
import os
from datetime import datetime, date
from task import Task

TASKS_FILE = "tasks.json"

def load_tasks():
    # Create file if doesn't exist
    if not os.path.exists(TASKS_FILE):
        print(f"Debug: {TASKS_FILE} does not exist. Creating a new file.")
        # Initialize with an empty list
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
        print(f"Debug: Initialized {TASKS_FILE} with an empty task list.")
    except IOError as e:
        print(f"Could not create {TASKS_FILE}. Check permissions: {e}")
        return []
    
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            if not isinstance(tasks_data, list):
                print(f"Warning: {TASKS_FILE} contains invalid data format.Resetting tasks.")
            
            return []
        loaded_tasks = []
        for t in tasks_data:
                try:
                    task_obj = Task(
                        t['id'],
                        t['title'],
                        t['description'],
                        t.get('due_date'),
                        t.get('completed', False)
                    )
                    loaded_tasks.append(task_obj)
                except KeyError as ke:
                    print(f"Error: Missing key in task data: {ke} for task: {t}")
                except Exception as ex:
                    print(f"Error: Error creating Task object: {ex} for task: {t}")
        return loaded_tasks
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {TASKS_FILE}. File might be corrupt and empty. Creating a new empty file.")
    try:
            with open(TASKS_FILE, 'w') as f:
                json.dump([], f)
    except IOError as e:
        print(f"Error: Could not create new empty {TASKS_FILE} after decode error: {e}")
        return []
    except Exception as e:
        print(f"Error: Could not read {TASKS_FILE}. Check file permissions: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading tasks: {e}")
        return []
  
def save_tasks(tasks):
    print(f"Debug: Attempting to save {len(tasks)} tasks to {TASKS_FILE}.")
    try:
        data_to_save = [t.to_dict() for t in tasks]
        with open(TASKS_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
            print(f"Debug: Successfully saved {len(tasks)} tasks.")  
    except IOError as e:
        print(f"Error: Could not write to {TASKS_FILE}. Check file permissions or disk space. Error: {e}")
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