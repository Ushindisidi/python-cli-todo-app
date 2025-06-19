import argparse
from utils import load_tasks, save_tasks, generate_new_id, validate_date, is_due_today
from task import Task

def add_task(tasks, title, description, due_date=None):
    validated_due_date = validate_date(due_date)
    if due_date and not validated_due_date:
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return
    new_id = generate_new_id(tasks)
    new_task = Task(
        id=new_id,
        title=title,
        description=description,
        due_date=validated_due_date
    )
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✓ Added task #{new_id}: {title}")
def list_tasks(tasks, show_today_only=False):
        filtered = tasks
        if show_today_only:
            filtered = [t for t in tasks if is_due_today(t)]
            if not filtered:
                print("No tasks found." if not show_today_only else "No tasks due today.")
                return
            print("\n--- Your Tasks ---")
            for task in filtered:
                print(task)
                print("---------------------\n")
def complete_task(tasks, task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id}'. Must be an integer.")
        return
    for task in tasks:
        if task.id == task_id:
            if task.completed:
                print(f"Task #{task_id} is already marked as complete.")
                return
            task.mark_complete()
            save_tasks(tasks)
            print(f"✓ Marked task #{task_id} as complete.")
            return
    print(f"Error: Task #{task_id} not found.")
def delete_task(tasks, task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id}'. Please provide a number.")
        return
    initial_task_count = len(tasks)
    tasks[:] = [task for task in tasks if task.id != task_id]
    if len(tasks) < initial_task_count:
        save_tasks(tasks)
        print(f"✓ Deleted task #{task_id}.")
    else:
        print(f"Error: Task #{task_id} not found.")
def main():
    tasks = load_tasks()
    parser = argparse.ArgumentParser(description="A simple CLI To-Do Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")
    add_parser.add_argument("description", type=str, help="Description of the task")
    add_parser.add_argument("-d", "--due", type=str, help="Optional due date (YYYY-MM-DD)", default=None)
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--today", action="store_true", help="List only tasks due today")
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=str, help="ID of the task to complete")
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=str, help="ID of the task to delete")
    args = parser.parse_args()
    if args.command == "add":
            add_task(tasks, args.title, args.description, args.due)
    elif args.command == "list":
            list_tasks(tasks, args.today)
    elif args.command == "complete":
            complete_task(tasks, args.id)
    elif args.command == "delete":
            delete_task(tasks, args.id)
    else:
            parser.print_help()
    
    if __name__ == "__main__":
        main()
        
    
    
     