import unittest
import os
import json
from datetime import date # Import date for is_due_today testing

# Import utils and Task
from utils import save_tasks, load_tasks, generate_new_id, validate_date, is_due_today, TASKS_FILE # Corrected generate_id to generate_new_id, added is_due_today, and TASKS_FILE
from task import Task

class TestUtils(unittest.TestCase):
    def setUp(self):
        """
        Set up for test methods. Creates a dummy test_tasks.json and patches
        the TASKS_FILE variable in utils to point to this test file.
        """
        self.test_file = "test_tasks.json"
        self.tasks = [
            Task(1, "Task 1", "Description 1"),
            Task(2, "Task 2", "Description 2", "2023-12-31", True), # Ensure this date is in the future relative to now
            Task(3, "Today's Task", "This task is due today", date.today().strftime("%Y-%m-%d"), False) # Task due today
        ]
        
        # Patch the TASKS_FILE for tests to use a temporary file
        # We need to import utils directly to modify its module-level variable
        import utils
        self.original_tasks_file = utils.TASKS_FILE
        utils.TASKS_FILE = self.test_file

        # Ensure the test file is clean before each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        # Save dummy data for tests that need it pre-loaded
        with open(self.test_file, 'w') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def tearDown(self):
        """
        Clean up after test methods. Removes the dummy test file and restores
        the original TASKS_FILE path in utils.
        """
        # Clean up test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        # Restore original TASKS_FILE path in utils
        import utils
        utils.TASKS_FILE = self.original_tasks_file

    def test_save_and_load(self):
        """
        Tests if tasks can be correctly saved to and loaded from the JSON file.
        """
        loaded = load_tasks()
        self.assertEqual(len(loaded), len(self.tasks))
        
        # Verify details of the first loaded task
        self.assertEqual(loaded[0].id, self.tasks[0].id)
        self.assertEqual(loaded[0].title, self.tasks[0].title)
        self.assertEqual(loaded[0].description, self.tasks[0].description)
        self.assertEqual(loaded[0].due_date, self.tasks[0].due_date)
        self.assertEqual(loaded[0].completed, self.tasks[0].completed)

        # Verify details of the second loaded task (with due date and completed status)
        self.assertEqual(loaded[1].id, self.tasks[1].id)
        self.assertEqual(loaded[1].title, self.tasks[1].title)
        self.assertEqual(loaded[1].description, self.tasks[1].description)
        self.assertEqual(loaded[1].due_date, self.tasks[1].due_date) # Corrected assertion
        self.assertEqual(loaded[1].completed, self.tasks[1].completed)

    def test_generate_new_id(self): # Corrected name to match utils
        """
        Tests the ID generation logic for new tasks.
        """
        self.assertEqual(generate_new_id([]), 1) # Test with an empty list
        self.assertEqual(generate_new_id([Task(1, "Test", "")]), 2) # Test with one task
        self.assertEqual(generate_new_id([Task(5, "Test", ""), Task(10, "Test2", "")]), 11) # Test with multiple tasks

    def test_validate_date(self):
        """
        Tests the date validation function.
        """
        self.assertEqual(validate_date("2023-12-31"), "2023-12-31") # Valid date
        self.assertIsNone(validate_date("2023-02-30"))  # Invalid day for February
        self.assertIsNone(validate_date("invalid-date")) # Malformed string
        self.assertIsNone(validate_date("2023/12/31")) # Wrong format
        self.assertIsNone(validate_date(None)) # Test with None input
        self.assertIsNone(validate_date("")) # Test with empty string input

    def test_is_due_today(self):
        """
        Tests the function that checks if a task is due today.
        """
        # Task due today
        today_task = [t for t in self.tasks if t.title == "Today's Task"][0]
        self.assertTrue(is_due_today(today_task))

        # Task not due today (future date)
        future_task = [t for t in self.tasks if t.title == "Task 2"][0]
        self.assertFalse(is_due_today(future_task))

        # Task with no due date
        no_due_date_task = [t for t in self.tasks if t.title == "Task 1"][0]
        self.assertFalse(is_due_today(no_due_date_task))

        # Task with an invalid due date format (should return False)
        invalid_date_task = Task(4, "Bad Date", "Description", "2023/10/05")
        self.assertFalse(is_due_today(invalid_date_task))


if __name__ == "__main__":
    unittest.main()