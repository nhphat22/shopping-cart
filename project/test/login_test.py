import json


def login_user(self, userName, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            userName=userName,
            password=password
        )),
        content_type='application/json',
    )
