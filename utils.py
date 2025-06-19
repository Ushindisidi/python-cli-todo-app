import json
import os
from datetime import datetime, date 
from task import Task 

TASKS_FILE = "tasks.json" 

def load_tasks():
    print(f"DEBUG (utils.load_tasks): Attempting to load tasks from {TASKS_FILE}")
    if not os.path.exists(TASKS_FILE):
        print(f"DEBUG (utils.load_tasks): {TASKS_FILE} does not exist. Creating empty file.")
        try:
            with open(TASKS_FILE, 'w') as f:
                json.dump([], f) # Initialize with an empty list to ensure valid JSON structure
            print(f"DEBUG (utils.load_tasks): {TASKS_FILE} created successfully with empty list.")
        except IOError as e:
            print(f"ERROR (utils.load_tasks): Could not create {TASKS_FILE}. Check permissions: {e}")
            return []
        return []

    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            print(f"DEBUG (utils.load_tasks): Successfully loaded raw data: {tasks_data}") # THIS IS KEY
            # Ensure tasks_data is a list before proceeding
            if not isinstance(tasks_data, list):
                print(f"Warning (utils.load_tasks): {TASKS_FILE} contains invalid data format. Resetting tasks.")
                return []
            
            # Reconstruct Task objects from the loaded data
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
                    print(f"ERROR (utils.load_tasks): Missing key in task data: {ke} for task: {t}")
                except Exception as ex:
                    print(f"ERROR (utils.load_tasks): Error creating Task object: {ex} for task: {t}")
            print(f"DEBUG (utils.load_tasks): Converted {len(loaded_tasks)} raw dicts to Task objects.")
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
    print(f"Debug: Current working directory: {os.getcwd()}") 
    print(f"Debug: Saving tasks to: {os.path.abspath(TASKS_FILE)}") 
  
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4) 
        print(f"DEBUG (utils.save_tasks): Successfully saved {len(tasks)} tasks.")
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