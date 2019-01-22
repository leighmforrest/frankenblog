from django.test import TestCase
from users.models import CustomUser


class TestCustomUser(TestCase):
    def test_user_string(self):
        user = CustomUser(username='eljefe')
        self.assertEqual(user.username, str(user))
