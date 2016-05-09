import sqlite3
import todo  # pylint: disable=import-error
from unittest import TestCase
from unittest.mock import patch


class ServerTestCase(TestCase):

    @patch('todo.debug')
    @patch('todo.run')
    def test_that_server_starts_properly(self, run_mock, debug_mock):
        # Given

        # When
        todo.main()

        # Then
        debug_mock.assert_called_once_with(True)
        run_mock.assert_called_once_with(reloader=True, host='localhost', port=8080)


class TodoListTestCase(TestCase):

    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
        self.db.execute("INSERT INTO todo (task,status) VALUES ('Task 1',1)")
        self.db.execute("INSERT INTO todo (task,status) VALUES ('Task 2',0)")
        self.db.commit()

    def tearDown(self):
        try:
            self.db.close()
        except sqlite3.ProgrammingError:
            pass

    @patch('todo.sqlite3.connect')
    def test_html_response_contains_correct_tasks(self, connect_mock):
        # Given
        connect_mock.return_value = self.db

        # When
        response = todo.todo_list()

        # Then
        self.assertTrue('<td>1</td>' in response)
        self.assertTrue('<td>Task 1</td>' in response)
        self.assertFalse('<td>2</td>' in response)
        self.assertFalse('<td>Task 2</td>' in response)


class NewTodoTestCase(TestCase):

    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
        self.db.execute("INSERT INTO todo (task,status) VALUES ('Task 1',1)")
        self.db.execute("INSERT INTO todo (task,status) VALUES ('Task 2',0)")
        self.db.commit()

    def tearDown(self):
        try:
            self.db.close()
        except sqlite3.ProgrammingError:
            pass

    @patch('todo.sqlite3.connect')
    def test_shows_new_todo_form(self, connect_mock):
        # Given
        connect_mock.return_value = self.db

        # When
        response = todo.new_item()

        # Then
        self.assertGreater(len(response), 0)

    @patch('todo.request')
    @patch('todo.sqlite3.connect')
    def test_adds_new_todo(self, connect_mock, request_mock):
        # Given
        connect_mock.return_value = self.db
        request_mock.GET = {'save': 'save', 'task': 'Task 3'}

        # When
        response = todo.new_item()

        # Then
        c = self.db.cursor()
        c.execute("SELECT status from todo WHERE task='Task 3'")
        result = c.fetchone()

        self.assertTrue(result)
        self.assertEqual(result[0], 1)
        self.assertTrue('the id is 3' in response)


class EditTodoTestCase(TestCase):

    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
        self.db.execute("INSERT INTO todo (task,status) VALUES ('Task 1',1)")
        self.db.execute("INSERT INTO todo (task,status) VALUES ('Task 2',0)")
        self.db.commit()

    def tearDown(self):
        try:
            self.db.close()
        except sqlite3.ProgrammingError:
            pass

    @patch('todo.sqlite3.connect')
    def test_shows_edit_todo_form(self, connect_mock):
        # Given
        connect_mock.return_value = self.db

        # When
        response = todo.edit_item(1)

        # Then
        self.assertTrue('action="/edit/1"' in response)
        self.assertTrue('value="Task 1"' in response)

    @patch('todo.request')
    @patch('todo.sqlite3.connect')
    def test_edit_todo(self, connect_mock, request_mock):
        # Given
        connect_mock.return_value = self.db
        request_mock.GET = {'save': 'save', 'task': 'Task 1 edited', 'status': 'close'}

        # When
        response = todo.edit_item(1)

        # Then
        c = self.db.cursor()
        c.execute("SELECT status from todo WHERE task='Task 1 edited'")
        result = c.fetchone()

        self.assertTrue(result)
        self.assertEqual(result[0], 0)
        self.assertTrue('item number 1' in response)
