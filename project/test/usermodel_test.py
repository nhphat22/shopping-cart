import unittest
from project.server import db
from project.server.models.user_model import User
from project.test.base_testcase import BaseTestCase

class TestUserModel(BaseTestCase):
    def test_encode_auth_token(self):
        user = User(
            userName='test',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id).encode("utf-8")  

        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            userName='test',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id).encode("utf-8")

        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()