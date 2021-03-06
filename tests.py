#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json, jsonify
from config import basedir
from app import app, db, bcrypt, models, users
from app.models import User, Card, Profile, ROLE_ADMIN
from app.users import authenticate_by_email, authenticate_by_id

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
       
        # Create two mock users
        johndoe = User(firstName = "John",
                       lastName = "Doe",
                       email = "johndoe@umbc.edu",
                       password = bcrypt.generate_password_hash("password1"),
                       university = "UMBC",
                       role = ROLE_ADMIN,
                       courses = ",".join(["CMSC 304", "CMSC 345", "CMSC 331", "STAT 355"]))
        johndoe.profile = Profile(grad_year = "2015",
                                  major = "Computer Science",
                                  bio = "I'm a nobody.",
                                  avatar = "")

        janedoe = User(firstName = "Jane",
                       lastName = "Doe",
                       password = bcrypt.generate_password_hash("password2"),
                       university = "UMBC",
                       courses = ",".join(["CMSC 304", "CMSC 341", "CMSC 313", "STAT 355"]))
        janedoe.profile = Profile(grad_year = "2016",
                                  major = "Computer Science",
                                  bio = "I'm nobody's sister.",
                                  avatar = "")
 
        db.session.add(johndoe)
        db.session.add(janedoe)
        
        db.session.commit()

        #from test_add_card_valid_min
        response = self.app.post('/deku/api/cards', data=dict(
                                                        user="janedoe@email.edu",
                                                        pwd="jane",
                                                        content="content1",
                                                        category="cat",
                                                        tags=["one","two"],
                                                        comments=['','comment 2','comment 3']))
        
        
        response = self.app.post('/deku/api/cards', data=dict(
                                                        user="janedoe@email.edu",
                                                        pwd="jane",
                                                        content="content2",
                                                        category="cat",
                                                        tags=["one"]))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_users_status(self):
        response = self.app.get('/deku/api/users')
        self.assertEquals(response.status_code, 200)

    def test_get_users_data(self):
        response = self.app.get('/deku/api/users')
        assert "John" in response.data

    def test_post_user_already_exists(self):
        response = self.app.post('/deku/api/users', data = dict(email = "johndoe@umbc.edu"))
        self.assertEquals(response.status_code, 400)

    def test_post_user_missing_fields(self):
        response = self.app.post('/deku/api/users')
        self.assertEquals(response.status_code, 400)

    def test_post_user_success(self):
        response = self.app.post('/deku/api/users',
        data = dict(firstName = "Jeremy",
                    lastName = "Neal",
                    password = "mypassword",
                    email = "jneal2@umbc.edu",
                    university = "UMBC",
                    grad_year = "2015",
                    major = "Computer Science",
                    classes = json.dumps(["CMSC 304", "CMSC 345", "CMSC 331", "STAT 355"]),
                    bio = "I make things."))
        self.assertEquals(response.status_code, 201)

    def test_make_admin_success(self):
        response = self.app.put('/deku/api/users/make_admin/1')
        self.assertEquals(response.status_code, 200)

    def test_make_admin_user_doesnt_exist(self):
        response = self.app.put('/deku/api/users/make_admin/456')
        self.assertEquals(response.status_code, 404)

    def test_get_user_by_id_success(self):
        response = self.app.get('/deku/api/users/1')
        assert "John" in response.data

    def test_get_user_by_id_user_doesnt_exist(self):
        response = self.app.get('/deku/api/users/456')
        self.assertEquals(response.status_code, 404)

    def test_put_user_by_id_invalid_password(self):
        response = self.app.put('/deku/api/users/1', data = dict(confirm_password="wrongpassword"))
        self.assertEquals(response.status_code, 401)

    def test_put_user_by_id_success(self):
        response = self.app.put('/deku/api/users/1', data = dict(confirm_password="password1",
                                                                 bio = "I'm a somebody."))
        assert "I'm a somebody." in response.data

    def test_delete_user_by_id_user_is_admin_cannot_delete_own_account(self):
        response = self.app.delete('/deku/api/users/1', data = dict(password="password1"))
        self.assertEquals(response.status_code, 403)

    def test_delete_user_by_id_success(self):
        response = self.app.delete('/deku/api/users/2', data = dict(password="password2"))
        self.assertEquals(response.status_code, 200) 
      
if __name__ == '__main__':
    unittest.main()
