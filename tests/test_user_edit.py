import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    change_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            "Wrong name of the user after edit"
        )

    @pytest.mark.parametrize('param', change_params)
    def test_edit_user_details_not_auth(self, param):
        # EDIT
        if param == 'email':
            value = 'test2@example.com'
        else:
            value = 'qwerty'
        response = MyRequests.put(
            f"/user/2",
            data={param: value}
        )
        Assertions.assert_code_status(response, 400)

    @pytest.mark.parametrize('param', change_params)
    def test_edit_user_details_auth_as_other_user(self, param):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
         }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        if param == 'email':
            data[param] = 'test2@example.com'
        else:
            data[param] = 'qwerty'
        response2 = MyRequests.put(
            "/user/99224",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=data
        )
        Assertions.assert_code_status(response2, 400)

    def test_edit_this_user_email(self):
        # LOGIN
        login_data = {
            "password": "12345",
            "email": "test_irina_12@example.com"
        }
        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # EDIT
        new_email = "test_irina_12example.com"
        response2 = MyRequests.put(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response2, 400)

    def test_edit_this_user_firstname_to_short(self):
        # LOGIN
        login_data = {
            "password": "12345",
            "email": "test_irina_12@example.com"
        }
        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # EDIT
        new_first_name = "L"
        response2 = MyRequests.put(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )
        Assertions.assert_code_status(response2, 400)
