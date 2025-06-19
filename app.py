import argparse
# No longer directly importing datetime here, as is_due_today handles it via utils
from utils import load_tasks, save_tasks, generate_new_id, validate_date, is_due_today # Adjusted generate_id to generate_new_id and added is_due_today
from task import Task

def add_task(tasks, title, description, due_date=None):
    """
    Adds a new task to the list.
    """
    validated_due_date = validate_date(due_date)
    if due_date and not validated_due_date: # Only print error if user actually provided a due date
        print("Error: Invalid due date format. Please use YYYY-MM-DD.")
        return

    new_id = generate_new_id(tasks) # Call the renamed function
    new_task = Task(
        id=new_id,
        title=title,
        description=description,
        due_date=validated_due_date # Use the validated date
    )
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✓ Added task #{new_id}: {title}")

def list_tasks(tasks, show_today_only=False):
    """
    Lists all tasks or only tasks due today.
    """
    print(f"DEBUG (app.list_tasks): list_tasks called with {len(tasks)} tasks.")
    filtered = tasks

    if show_today_only:
        filtered = [t for t in tasks if is_due_today(t)] # Use the utility function
        print(f"DEBUG (app.list_tasks): Filtered for today, {len(filtered)} tasks remain.")

    if not filtered:
        print("No tasks found." if not show_today_only else "No tasks due today.")
        return

    print("\n--- Your Tasks ---")
    for task in filtered:
        print(task)
        # Removed the separator line after each task for cleaner output, as Task._str_ is detailed
    print("-------------------\n")


def complete_task(tasks, task_id):
    """
    Marks a task as completed.
    """
    try:
        task_id = int(task_id) # Ensure ID is integer
    except ValueError:
        print(f"Error: Invalid task ID '{task_id}'. Please provide a number.")
        return

    for task in tasks:
        if task.id == task_id:
            if task.completed:
                print(f"Task #{task_id} is already completed.")
                return
            task.mark_complete()
            save_tasks(tasks)
            print(f"✓ Marked task #{task_id} as complete.")
            return
    print(f"Error: Task #{task_id} not found.")

def delete_task(tasks, task_id):
    """
    Deletes a task by ID.
    """
    try:
        task_id = int(task_id) # Ensure ID is integer
    except ValueError:
        print(f"Error: Invalid task ID '{task_id}'. Please provide a number.")
        return

    initial_task_count = len(tasks)
    # Using list comprehension for deletion is cleaner and safer than direct index deletion within a loop
    tasks[:] = [task for task in tasks if task.id != task_id] # This modifies the list in place

    if len(tasks) < initial_task_count:
        save_tasks(tasks)
        print(f"✓ Deleted task #{task_id}.")
    else:
        print(f"Error: Task #{task_id} not found.")


def main():
    """
    Main function to parse command-line arguments and execute commands.
    """
    tasks = load_tasks()
    print(f"DEBUG (app.main): Loaded {len(tasks)} tasks at start.")
    parser = argparse.ArgumentParser(description="A simple CLI To-Do Manager.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")
    add_parser.add_argument("description", type=str, help="Description of the task")
    add_parser.add_argument("-d", "--due", type=str, help="Optional due date (YYYY-MM-DD)", default=None)

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--today", action="store_true", help="List only tasks due today")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=str, help="ID of the task to complete") # Keep as str for validation in function

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=str, help="ID of the task to delete") # Keep as str for validation in function

    args = parser.parse_args()

    # Dispatch commands to their respective functions
    if args.command == "add":
        add_task(tasks, args.title, args.description, args.due)
    elif args.command == "list":
        list_tasks(tasks, args.today)
    elif args.command == "complete":
        complete_task(tasks, args.id)
    elif args.command == "delete":
        delete_task(tasks, args.id)
    else:
        # This block should technically not be reached if required=True for subparsers
        parser.print_help()

if __name__ == "__main__": 
    main()