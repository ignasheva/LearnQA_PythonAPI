import pytest
from string import ascii_lowercase
from random import choices
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    exclude_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected content {response.content}"

    def test_create_user_with_invalid_email(self):
        email = 'testovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == "Invalid email format", f"Unexpected content {response.content}"

    @pytest.mark.parametrize('field', exclude_params)
    def test_create_user_without_one_field(self, field):
        data = self.prepare_registration_data()
        data.pop(field)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"The following required params are missed: {field}", f"Unexpected content {response.content}"

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = ''.join(choices(ascii_lowercase, k=1))
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"The value of 'username' field is too short", f"Unexpected content {response.content}"

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = ''.join(choices(ascii_lowercase, k=251))
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"The value of 'username' field is too long", f"Unexpected content {response.content}"
