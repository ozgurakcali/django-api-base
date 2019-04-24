from django.test import TestCase, Client
from faker import Factory


class BaseTests(TestCase):
    """
    Base class for test, providing common helper functions
    """

    def setUp(self):
        self.client = Client()
        self.faker = Factory.create()

    def _get_token(self, username, password):
        """
        Helper method to get token for a user
        """

        response = self.client.post('/login/', data={
            'username': username,
            'password': password
        })

        return response.get('x-authtoken')

    def _create_user(self):
        """
        Helper method to create a user
        """

        username = self.faker.email()
        password = self.faker.password(length=10)
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'username': username,
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)
        return response.json()['id'], username, password
