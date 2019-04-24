from django.test import Client
from faker import Factory

from authentication.models import JwtToken
from common.tests import BaseTests
from profiles.constants import Messages, RoleTypes
from profiles.models import User, Role, UserRole


class UserTests(BaseTests):
    """
    Tests for user profile operations
    """

    def setUp(self):
        self.client = Client()
        self.faker = Factory.create()

        # Set tokens for an END_USER,  USER_MANAGER and ADMINISTRATOR
        end_user = User.objects.create_user(username=self.faker.email(),
                                            email=self.faker.email(), password=self.faker.password(length=10))
        UserRole.objects.create(user=end_user, role=Role.objects.get(type=RoleTypes.END_USER))
        self.end_user_token = JwtToken.objects.create(token=JwtToken.generate_jwt_token(end_user)).token

        administrator = User.objects.create_user(username=self.faker.email(),
                                                 email=self.faker.email(), password=self.faker.password(length=10))
        UserRole.objects.create(user=administrator, role=Role.objects.get(type=RoleTypes.ADMINISTRATOR))
        self.administrator_token = JwtToken.objects.create(token=JwtToken.generate_jwt_token(administrator)).token

    def test_create_with_valid_data(self):
        """
        We should be able to create a user with valid data
        """

        password = self.faker.password(length=10)
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'username': self.faker.email(),
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)

    def test_create_with_missing_data(self):
        """
        We should NOT be able to create a user with providing missing data
        """

        password = self.faker.password(length=10)
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 400)

    def test_create_with_missing_password(self):
        """
        We should NOT be able to create a user without providing a password and password_confirm"""

        password = self.faker.password(length=10)
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'username': self.faker.email(),
            'password': password
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(Messages.USER__PASSWORD_MISSING,
                      [message['key'] for message in response.json()['messages']])

    def test_create_with_non_matching_passwords(self):
        """
        We should NOT be able to create a user with non-matching passwords
        """

        password = self.faker.password(length=10)
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'username': self.faker.email(),
            'password': password,
            'password_confirm': password + '_'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(Messages.USER__PASSWORDS_DO_NOT_MATCH,
                      [message['key'] for message in response.json()['messages']])

    def test_create_with_existing_username(self):
        """
        We should NOT be able to create a user with an existing username
        """

        password = self.faker.password(length=10)
        username = self.faker.email()
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'username': username,
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)

        # Now try to create a user with same username
        response = self.client.post('/users/', data={
            'first_name': self.faker.name(),
            'last_name': self.faker.name(),
            'email': self.faker.email(),
            'username': username,
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        """
        We should be able to update user data with the user itself, with an administrator or with a user manager
        """

        password = self.faker.password(length=10)
        initial_first_name = self.faker.name()
        initial_last_name = self.faker.name()
        username = self.faker.email()
        response = self.client.post('/users/', data={
            'first_name': initial_first_name,
            'last_name': initial_last_name,
            'email': self.faker.email(),
            'username': username,
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['body']['first_name'], initial_first_name)
        self.assertEqual(response.json()['body']['last_name'], initial_last_name)

        user_id = response.json()['body']['id']

        # Now get token for this user
        token = self._get_token(username, password)

        # Now try to update this user's data with self token
        updated_first_name = self.faker.name()
        updated_last_name = self.faker.name()
        response = self.client.put(
            '/users/' + str(user_id) + '/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token,
            data={
                'id': user_id,
                'first_name': updated_first_name,
                'last_name': updated_last_name,
                'email': self.faker.email(),
                'username': username,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body']['first_name'], updated_first_name)
        self.assertEqual(response.json()['body']['last_name'], updated_last_name)

        # Now try to create update this user's data with administrator token
        updated_first_name = self.faker.name()
        updated_last_name = self.faker.name()
        response = self.client.put(
            '/users/' + str(user_id) + '/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.administrator_token,
            data={
                'id': user_id,
                'first_name': updated_first_name,
                'last_name': updated_last_name,
                'email': self.faker.email(),
                'username': username,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body']['first_name'], updated_first_name)
        self.assertEqual(response.json()['body']['last_name'], updated_last_name)

    def test_update_without_authorization(self):
        """
        We should NOT be able to update a user while unauthenticated or authenticated with a different end user
        """

        password = self.faker.password(length=10)
        initial_first_name = self.faker.name()
        initial_last_name = self.faker.name()
        username = self.faker.email()
        response = self.client.post('/users/', data={
            'first_name': initial_first_name,
            'last_name': initial_last_name,
            'email': self.faker.email(),
            'username': username,
            'password': password,
            'password_confirm': password
        })
        self.assertEqual(response.status_code, 201)
        user_id = response.json()['body']['id']

        # Now try to update this user without authentication
        response = self.client.put(
            '/users/' + str(user_id) + '/',
            content_type='application/json',
            data={
                'id': user_id,
                'first_name': initial_first_name,
                'last_name': initial_last_name,
                'email': self.faker.email(),
                'username': username,
            }
        )
        self.assertEqual(response.status_code, 403)

        # Now try to update this user with another user's token
        response = self.client.put(
            '/users/' + str(user_id) + '/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.end_user_token,
            data={
                'id': user_id,
                'first_name': initial_first_name,
                'last_name': initial_last_name,
                'email': self.faker.email(),
                'username': username,
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_list(self):
        """
        We should be able to list users with a USER_MANAGER or ADMINISTRATOR
        """

        # Create a user first
        self._create_user()

        # Now try to list users with an administrator
        response = self.client.get('/users/',
                                   HTTP_AUTHORIZATION='Bearer ' + self.administrator_token)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()['body']), 1)

    def test_list_without_authorization(self):
        """
        We should NOT be able to list users without a USER_MANAGER or ADMINISTRATOR
        """

        # Create a user first
        self._create_user()

        # Now try to list users without authentication
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 403)

        # Now try to list users with an end user token
        response = self.client.get('/users/',
                                   HTTP_AUTHORIZATION='Bearer ' + self.end_user_token)
        self.assertEqual(response.status_code, 403)

    def test_retrieve(self):
        """
        We should be able to retrieve a user
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Now get token for this user
        token = self._get_token(username, password)

        # Now try to retrieve this user
        response = self.client.get('/users/' + str(user_id) + '/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body']['username'], username)

        # Now try to retrieve this user with an administrator
        response = self.client.get('/users/' + str(user_id) + '/',
                                   HTTP_AUTHORIZATION='Bearer ' + self.administrator_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body']['username'], username)

    def test_retrieve_without_authorization(self):
        """
        We should NOT be able to retrieve a user while unauthenticated or authenticated with a different end user
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Now try to retrieve this user without authentication
        response = self.client.get('/users/' + str(user_id) + '/')
        self.assertEqual(response.status_code, 403)

        # Now try to retrieve this user with another user's token
        response = self.client.get('/users/' + str(user_id) + '/',
                                   HTTP_AUTHORIZATION='Bearer ' + self.end_user_token)
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """
        We should be able to delete a user as the user itself, as a user manager or as an administrator
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Get token for the user
        token = self._get_token(username, password)

        # Now try to delete this user
        response = self.client.delete('/users/' + str(user_id) + '/',
                                      HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 204)

        # Now create another user
        user_id, username, password = self._create_user()

        # Now try to delete this meal with an administrator
        response = self.client.delete('/users/' + str(user_id) + '/',
                                      HTTP_AUTHORIZATION='Bearer ' + self.administrator_token)
        self.assertEqual(response.status_code, 204)

    def test_delete_without_authorization(self):
        """
        We should NOT be able to delete a meal without authentication or as another end user
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Now try to delete this user without authentication
        response = self.client.delete('/users/' + str(user_id) + '/')
        self.assertEqual(response.status_code, 403)

        # Now try to delete this user as another end user
        response = self.client.delete('/users/' + str(user_id) + '/',
                                      HTTP_AUTHORIZATION='Bearer ' + self.end_user_token)
        self.assertEqual(response.status_code, 403)

    def test_password_update(self):
        """
        We should be able to update user password with the user itself, with an administrator or with a user manager
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Now get token for this user
        token = self._get_token(username, password)

        # Now try to update this user's password with self token
        updated_password_1 = self.faker.password()
        response = self.client.put(
            '/users/' + str(user_id) + '/passwords/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token,
            data={
                'current_password': password,
                'password': updated_password_1,
                'password_confirm': updated_password_1
            }
        )
        self.assertEqual(response.status_code, 200)

        # Now try to update this user's password with administrator token
        updated_password_2 = self.faker.password()
        response = self.client.put(
            '/users/' + str(user_id) + '/passwords/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.administrator_token,
            data={
                'current_password': updated_password_1,
                'password': updated_password_2,
                'password_confirm': updated_password_2
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_password_update_with_invalid_data(self):
        """
        We should NOT be able to update user password providing invalid request data
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Now get token for this user
        token = self._get_token(username, password)

        # Now try to update this user's password with a wrong current password
        updated_password = self.faker.password()
        response = self.client.put(
            '/users/' + str(user_id) + '/passwords/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token,
            data={
                'current_password': password + '_',
                'password': updated_password,
                'password_confirm': updated_password
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(Messages.USER__INVALID_PASSWORD,
                      [message['key'] for message in response.json()['messages']])

        # Now try to update this user's password with a non-matching passwords
        updated_password = self.faker.password()
        response = self.client.put(
            '/users/' + str(user_id) + '/passwords/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token,
            data={
                'current_password': password,
                'password': updated_password,
                'password_confirm': updated_password + '_'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(Messages.USER__PASSWORDS_DO_NOT_MATCH,
                      [message['key'] for message in response.json()['messages']])

    def test_update_password_without_authorization(self):
        """
        We should NOT be able to update a user's password while unauthenticated or authenticated
        with a different end user
        """

        # Create a user first
        user_id, username, password = self._create_user()

        # Now try to update this user's password without authentication
        updated_password = self.faker.password()
        response = self.client.put(
            '/users/' + str(user_id) + '/passwords/',
            content_type='application/json',
            data={
                'current_password': password,
                'password': updated_password,
                'password_confirm': updated_password
            }
        )
        self.assertEqual(response.status_code, 403)

        # Now try to update this user's password with another user's token
        updated_password = self.faker.password()
        response = self.client.put(
            '/users/' + str(user_id) + '/passwords/',
            HTTP_AUTHORIZATION='Bearer ' + self.end_user_token,
            content_type='application/json',
            data={
                'current_password': password,
                'password': updated_password,
                'password_confirm': updated_password
            }
        )
        self.assertEqual(response.status_code, 403)


class UserRoleTests(BaseTests):
    """
    Tests for user role operations
    """

    def setUp(self):
        self.client = Client()
        self.faker = Factory.create()

        # Get administrator role object
        self.administrator_role = Role.objects.get(type=RoleTypes.ADMINISTRATOR)

        # Set token for super user
        super_user = User.objects.create_user(username=self.faker.email(),
                                              email=self.faker.email(), password=self.faker.password(length=10))
        super_user.is_superuser = True
        super_user.save()

        self.super_user_token = JwtToken.objects.create(token=JwtToken.generate_jwt_token(super_user)).token

    def test_create_with_valid_data(self):
        """
        We should be able to create a user role with valid data
        """

        user_id, username, password = self._create_user()

        # Now try to add administrator role to this user
        response = self.client.post('/user-roles/', data={
            'user': user_id,
            'role': self.administrator_role.id
        }, HTTP_AUTHORIZATION='Bearer ' + self.super_user_token)
        self.assertEqual(response.status_code, 201)

    def test_create_with_missing_data(self):
        """
        We should NOT be able to create a user role with missing data
        """

        user_id, username, password = self._create_user()

        # Now try to add administrator role to this user
        response = self.client.post('/user-roles/', data={
            'user': user_id
        }, HTTP_AUTHORIZATION='Bearer ' + self.super_user_token)
        self.assertEqual(response.status_code, 400)

    def test_create_without_authorization(self):
        """
        We should be NOT able to create a user role without required authorization
        """

        user_id, username, password = self._create_user()

        # Now try to add administrator role to this user without authentication
        response = self.client.post('/user-roles/', data={
            'user': user_id,
            'role': self.administrator_role.id
        })
        self.assertEqual(response.status_code, 403)

        # Now try to add administrator role to this user with an end user token
        token = self._get_token(username, password)

        response = self.client.post('/user-roles/', data={
            'user': user_id,
            'role': self.administrator_role.id
        }, HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 403)
