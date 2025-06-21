import json
import os
from datetime import datetime, date 
from task import Task 

TASKS_FILE = "tasks.json" 

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'w') as f:
                json.dump([], f) 
        except IOError as e:
            return []
        return []

    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            if not isinstance(tasks_data, list):
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
                except (KeyError, Exception):
                    continue
            return loaded_tasks

    except json.JSONDecodeError as jde: 
        print(f"ERROR (utils.load_tasks): Could not decode JSON from {TASKS_FILE}. File might be corrupted or empty. Error: {jde}")
        try:
            with open(TASKS_FILE, 'w') as f:
                json.dump([], f)
        except IOError as e:
            print(f"ERROR (utils.load_tasks): Could not create new empty {TASKS_FILE} after decode error: {e}")
        return []
    except IOError as e: # Catch file I/O errors
        print(f"ERROR (utils.load_tasks): Could not read {TASKS_FILE}. Check file permissions: {e}")
        return []
    except Exception as e:
        print(f"An unexpected ERROR occurred while loading tasks: {e}")
        return []

def save_tasks(tasks):
    import os
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4) 
    except IOError as e: 
        print(f"ERROR (utils.save_tasks): Could not write to {TASKS_FILE}. Check file permissions or disk space. Error: {e}")
    except Exception as e:
        print(f"An unexpected ERROR occurred while saving tasks: {e}")

    
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