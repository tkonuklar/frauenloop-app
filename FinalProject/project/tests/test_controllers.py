from project import app, db
from project.models import User
import unittest
import os
import json

class TestController(unittest.TestCase):

    #### setup and teardown ####

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    #### helper ####
    def create_user(self):
        user = User(name="Test",pin=1234)
        db.session.add(user)
        db.session.commit()
        return user

    #### tests ####
    def test_create_user(self):
        mock_request_data = {
            'name': 'Test User',
            'pin': 1234
            }
        response = self.app.post('/users', data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'],"Test User")
        self.assertEqual(data['pin'],1234)

    def test_get_users(self):
        user = self.create_user()
        response = self.app.get('/users')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['name'],user.name)
        self.assertEqual(data[0]['pin'],user.pin)

    def test_get_users_by_id(self):
        user = self.create_user()
        response = self.app.get(f'/users/{user.id}')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'],user.name)
        self.assertEqual(data['pin'],user.pin)

    def test_get_users_by_id_404(self):
        user = self.create_user()
        response = self.app.get(f'/users/{user.id+1}')
        self.assertEqual(response.status_code,404)


    def test_update_users(self):
        user = self.create_user()
        mock_request_data = {
            'name': 'Updated Test',
            'pin': 1235
            }
        response = self.app.put(f'/users/{user.id}',  data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'],"Updated Test")
        self.assertEqual(data['pin'],1235)

    def test_update_users_404(self):
        user = self.create_user()
        mock_request_data = {
            'name': 'Updated Test',
            'pin': 1235
            }
        response = self.app.put(f'/users/{user.id+1}',  data=json.dumps(mock_request_data))
        self.assertEqual(response.status_code,404)

    def test_delete_users(self):
        user = self.create_user()
        response = self.app.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code,204)
        self.assertEqual(response.get_data(as_text=True),"")

if __name__ == '__main__':
    unittest.main()