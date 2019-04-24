import json

from authentication.constants import Messages
from common.tests import BaseTests


class LoginTests(BaseTests):
    """
    Tests for login service
    """

    def test_login_with_valid_credentials(self):
        """
        We should be able to login with valid credentials
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Try to login with this user's credentials
        response = self.client.post('/login/', data={
            'username': username,
            'password': password
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('x-authtoken', response)

    def test_login_with_missing_data(self):
        """
        We should NOT be able to login providing missing data in the request
        """

        response = self.client.post('/login/', data={
            'username': self.faker.email()
        })

        self.assertEqual(response.status_code, 400)

    def test_login_with_invalid_credentials(self):
        """
        We should NOT be able to login with invalid credentials
        """

        # Try to login with a random username and password
        response = self.client.post('/login/', data={
            'username': self.faker.email(),
            'password': self.faker.password(length=5)
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn(Messages.TOKEN__AUTHENTICATION_FAILED,
                      [message['key'] for message in json.loads(response['Messages'])])


class MeTests(BaseTests):
    """
    Tests for me service
    """

    def test_get_me_with_valid_token(self):
        """
        We should be able to get currently logged in user with a valid token
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Get token for the user
        token = self._get_token(username, password)

        response = self.client.get('/me/', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], username)

    def test_get_me_without_token(self):
        """
        We should get a 403 status code without a token in the request
        """

        response = self.client.get('/me/')
        self.assertEqual(response.status_code, 403)


class LogoutTests(BaseTests):
    """
    Tests for logout service
    """

    def test_get_me_with_valid_token(self):
        """
        We should be able to log out with a valid token present
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Get token for the user
        token = self._get_token(username, password)

        response = self.client.post('/logout/', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 200)

    def test_get_me_without_token(self):
        """
        We should get a 403 status code without a token in the request
        """

        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 403)
