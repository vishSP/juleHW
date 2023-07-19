from rest_framework.test import APITestCase

from users.models import User


class SetupTestCase(APITestCase):
    def setUp(self):
        self.user = User(email='test@test.ru', phone='111111111', city='Testograd', is_superuser=True, is_staff=True,
                         is_active=True)
        self.user.set_password('123QWE456RTY')
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {"email": "test@test.ru", "password": "123QWE456RTY"}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


