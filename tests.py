import unittest
from unittest import mock

import worklog

class TestEntry(unittest.TestCase):
    def setUp(self):
        worklog.initialize()
        self.employee_name = 'Timmy'
        self.task_name = 'test task'
        self.task_time = 30
        self.task_date = '06/04/2020'
        self.notes = 'Allow me to test your patience..'

        try:
            self.test_entry = worklog.Entry.get(worklog.Entry.employee_name=='Timmy')
        except worklog.DoesNotExist:
            self.test_entry = worklog.Entry.create(
                employee_name = self.employee_name,
                task_name = self.task_name,
                task_time = self.task_time,
                task_date = self.task_date,
                notes = self.notes
            )

    def tearDown(self):
        try:
            self.test_entry.delete_instance()
        except worklog.DoesNotExist:
            pass

        try:
            worklog.db.close()
        except worklog.OperationalError:
            pass

    def test_entry_table_exists(self):
        assert worklog.Entry.table_exists()

    def test_employee_name(self):
        self.assertEqual(worklog.Entry.employee_name, self.employee_name)

    def test_task_name(self):
        self.assertEqual(worklog.Entry.task_name, self.task_name)

    def test_task_time(self):
        self.assertEqual(worklog.Entry.task_time, self.task_time)

    def test_task_date(self):
        self.assertEqual(worklog.Entry.task_date, self.task_date)

    def test_notes(self):
        self.assertEqual(worklog.Entry.notes, self.notes)       


if __name__ == '__main__':
    unittest.main()
