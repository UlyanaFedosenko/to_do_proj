import unittest
from unittest.mock import patch
from app import app

from sqlalchemy.exc import IntegrityError


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'user_name': 'johndoe',
            'password': 'password'
        }
        self.credentials = {
            'user_name': 'johndoe',
            'password': 'password'
        }

    @patch('app.session.add')
    @patch('app.session.commit')
    def test_register_success(self, mock_commit, mock_add):
        mock_commit.return_value = None
        mock_add.return_value = None
        response = self.client.post('/register', json=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'User created successfully'})

    @patch('app.session.add')
    @patch('app.session.commit')
    def test_register_failure_username_exists(self, mock_commit, mock_add):
        mock_commit.side_effect = IntegrityError('mock error', params=None, orig=BaseException)
        mock_add.return_value = None
        response = self.client.post('/register', json=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'Username already exists'})



if __name__ == '__main__':
    unittest.main()


