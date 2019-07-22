from project import app,db
from project.models import User
import unittest
import json


class TestController(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        db.drop_all()
        db.create_all()
        self.app = app.test_client()
        self.assertEqual(app.debug,False)

    def tearDown(self):
        pass

    def create_user(self):
        user = User(name='Test User',pin='1234',balance=1000)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_user_by_id(self,id):
        return User.query.filter_by(id=id).first()

    def test_create_user(self):
        mock_request_data = {
            'name': 'Test User',
            'pin': 1234,
            'balance': 1000
            }
        response = self.app.post('/users', data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['pin'], '1234')
        self.assertEqual(data['balance'], 1000)


    def test_get_users(self):
       mock_user = self.create_user()
       response = self.app.get('/users')
       data = json.loads(response.get_data(as_text=True))
       self.assertEqual(response.status_code, 200)
       self.assertEqual(data[0]['name'], mock_user.name)
       self.assertEqual(data[0]['pin'], mock_user.pin)
       self.assertEqual(data[0]['balance'], mock_user.balance)
    
    def test_delete_user(self):
        mock_user = self.create_user()
        response = self.app.delete(f'/users/{mock_user.id}')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(data,"")
        # Did it deleted frm DB too ?
        user = self.get_user_by_id(mock_user.id)
        self.assertIsNone(user)

    def test_get_user_by_id_404(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.id+1}')
        self.assertEqual(response.status_code,404)


        






