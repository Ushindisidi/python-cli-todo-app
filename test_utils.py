import unittest
import os
import json
from datetime import date 

from utils import save_tasks, load_tasks, generate_new_id, validate_date, is_due_today, TASKS_FILE 
from task import Task

class TestUtils(unittest.TestCase):
    def setUp(self):
       
        self.test_file = "test_tasks.json"
        self.tasks = [
            Task(1, "cooking", "rice and beef", "2024-01-01", False),
            Task(2, "braiding hair", "fulani braids", "2025-12-31", True),
            Task(3, "Today's Task", "This task is due today", date.today().strftime("%Y-%m-%d"), False)
        ]
        
        import utils
        self.original_tasks_file = utils.TASKS_FILE
        utils.TASKS_FILE = self.test_file

        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        print(f"\nDEBUG (setUp): Attempting to write {len(self.tasks)} tasks to {self.test_file}") # ADDED DEBUG
        try:
            with open(self.test_file, 'w') as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=4)
            print(f"DEBUG (setUp): Successfully wrote to {self.test_file}. Content check:") # ADDED DEBUG
            with open(self.test_file, 'r') as f_read: # ADDED DEBUG
                print(f_read.read()) # ADDED DEBUG: Print file content
        except Exception as e: # ADDED DEBUG
            print(f"ERROR (setUp): Failed to write to {self.test_file}: {e}") # ADDED DEBUG

    def tearDown(self):
        """
        Clean up after test methods. Removes the dummy test file and restores
        the original TASKS_FILE path in utils.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            print(f"DEBUG (tearDown): Removed {self.test_file}") # ADDED DEBUG
        
        import utils
        utils.TASKS_FILE = self.original_tasks_file

    def test_save_and_load(self):
        """
        Tests if tasks can be correctly saved to and loaded from the JSON file.
        """
        print(f"DEBUG (test_save_and_load): Calling load_tasks()") # ADDED DEBUG
        loaded = load_tasks()
        print(f"DEBUG (test_save_and_load): load_tasks returned {len(loaded)} tasks.") # ADDED DEBUG
        self.assertEqual(len(loaded), len(self.tasks))
        
        self.assertEqual(loaded[0].id, self.tasks[0].id)
        self.assertEqual(loaded[0].title, self.tasks[0].title)
        self.assertEqual(loaded[0].description, self.tasks[0].description)
        self.assertEqual(loaded[0].due_date, self.tasks[0].due_date)
        self.assertEqual(loaded[0].completed, self.tasks[0].completed)

        self.assertEqual(loaded[1].id, self.tasks[1].id)
        self.assertEqual(loaded[1].title, self.tasks[1].title)
        self.assertEqual(loaded[1].description, self.tasks[1].description)
        self.assertEqual(loaded[1].due_date, self.tasks[1].due_date)
        self.assertEqual(loaded[1].completed, self.tasks[1].completed)
        
        self.assertEqual(loaded[2].id, self.tasks[2].id)
        self.assertEqual(loaded[2].title, self.tasks[2].title)
        self.assertEqual(loaded[2].description, self.tasks[2].description)
        self.assertEqual(loaded[2].due_date, self.tasks[2].due_date)
        self.assertEqual(loaded[2].completed, self.tasks[2].completed)


    def test_generate_new_id(self): 
        self.assertEqual(generate_new_id([]), 1) 
        self.assertEqual(generate_new_id([Task(1, "Test", "")]), 2) 
        self.assertEqual(generate_new_id([Task(5, "Test", ""), Task(10, "Test2", "")]), 11) 

    def test_validate_date(self):
        self.assertEqual(validate_date("2023-12-31"), "2023-12-31") 
        self.assertIsNone(validate_date("2023-02-30"))  
        self.assertIsNone(validate_date("invalid-date")) 
        self.assertIsNone(validate_date("2023/12/31")) 
        self.assertIsNone(validate_date(None)) 
        self.assertIsNone(validate_date("")) 

    def test_is_due_today(self): 
        
        today_task = [t for t in self.tasks if t.title == "Today's Task"][0]
        self.assertTrue(is_due_today(today_task))

        future_task = [t for t in self.tasks if t.title == "braiding hair"][0] 
        self.assertFalse(is_due_today(future_task))

        no_due_date_task = Task(4, "No Due Date", "Description", None)
        self.assertFalse(is_due_today(no_due_date_task))

        invalid_date_task = Task(5, "Bad Date", "Description", "2023/10/05") 
        self.assertFalse(is_due_today(invalid_date_task))

    def test_is_due_today_various_cases(self):
       
        task_today = Task(10, "Due Today", "desc", date.today().strftime("%Y-%m-%d"))
        self.assertTrue(is_due_today(task_today))

        task_past = Task(11, "Past Task", "desc", "2000-01-01")
        self.assertFalse(is_due_today(task_past))

        future_date_obj = date.today().replace(year=date.today().year + 1)
        future_date = future_date_obj.strftime("%Y-%m-%d")
        task_future = Task(12, "Future Task", "desc", future_date)
        self.assertFalse(is_due_today(task_future))

        task_none = Task(13, "No Due Date", "desc", None)
        self.assertFalse(is_due_today(task_none))

        task_empty = Task(14, "Empty Due Date", "desc", "")
        self.assertFalse(is_due_today(task_empty))

        task_invalid = Task(15, "Invalid Date", "desc", "2024/01/01") 
        self.assertFalse(is_due_today(task_invalid))

        task_nondatestr = Task(16, "Nondatestr", "desc", "not-a-date")
        self.assertFalse(is_due_today(task_nondatestr))


if __name__ == "__main__":
    unittest.main()