from django.core.cache import cache
from unittest import mock
from rest_framework.test import APITestCase
from accounts.models import Profile


class TestVerifySmsCodeAPI(APITestCase):
    def setUp(self):
        self.user = Profile.objects.create(
            username="testuser",
            phone="+998999999999",
            user_id=str(6450190863),
        )

    @mock.patch("accounts.views.bot.get_chat")
    @mock.patch("accounts.views.cache.get")
    def test_verify_sms_code_success(self, mock_cache, mock_get_chat):
        mock_get_chat.return_value = self.user
        mock_cache.return_value = self.user.user_id
        sms_code = "323223"
        cache.set(sms_code, self.user.user_id, timeout=60)
        response = self.client.post("/api/accounts/verify-code/", data={"code": "323223"})

        self.assertEqual(response.status_code, 200)
        expected_data = {
            "message": "OK",
            "data": {
                "user_id": self.user.user_id,
                "username": self.user.username,
                "phone": self.user.phone
            },
        }
        self.assertDictEqual(response.json(), expected_data)

    @mock.patch("accounts.views.bot.get_chat")
    def test_with_invalid_code(self, mock_get_chat):
        mock_get_chat.return_value = self.user
        response = self.client.post("/api/accounts/verify-code/", data={"code": "456455"})

        self.assertEqual(response.status_code, 400)
        expected_data = {
            "message": "code_was_invalid_or_expired",
        }
        self.assertDictEqual(response.json(), expected_data)

    @mock.patch("accounts.views.cache.get")
    @mock.patch("accounts.views.bot.get_chat")
    def test_with_invalid_user_data(self, mock_get_chat, mock_cache):
        mock_cache.return_value = "123456789"
        fake_profile = Profile.objects.create(
            username="testuser1212",
            phone="+998999999999",
            user_id=str(645019121863),
            is_active=True
        )

        mock_get_chat.return_value = fake_profile
        response = self.client.post("/api/accounts/verify-code/", data={"code": "456455"})

        self.assertEqual(response.status_code, 404)
        expected_data = {
            "message": "profile_not_found",
        }
        self.assertDictEqual(response.json(), expected_data)
