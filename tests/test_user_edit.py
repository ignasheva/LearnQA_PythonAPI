import allure
import time
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    change_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    @allure.description(
        "The test verifies that it is possible to edit the newly created user profile"
    )
    @allure.tag("Edit", "Positive")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
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

    @allure.description(
        "The test checks that it is impossible to edit a user if you are not authorized"
    )
    @allure.tag("Edit", "Negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
    @pytest.mark.parametrize('param', change_params)
    def test_edit_user_details_not_auth(self, param):
        # EDIT
        if param == 'email':
            pass
        else:
            value = 'qwerty'
            response = MyRequests.put(
                f"/user/2",
                data={param: value}
            )
            Assertions.assert_code_status(response, 400)
            assert response.content.decode(
                'utf-8') == '{"error":"Auth token not supplied"}', f"Unexpected content {response.content}"

    @allure.description(
        "The test checks that it is impossible to edit a user if you are logged in as another user"
    )
    @allure.tag("Edit", "Negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
    @pytest.mark.parametrize('param', change_params)
    def test_edit_user_details_auth_as_other_user(self, param):
        # REGISTER USER 1
        data_user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data_user1)
        email = data_user1['email']
        password = data_user1['password']

        # REGISTER USER 2
        time.sleep(1)
        data_user2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=data_user2)
        user_id = self.get_json_value(response2, "id")

        # LOGIN BY USER 1
        data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # EDIT USER 2
        if param == 'email':
            data[param] = 'test_iit12@example.com'
        else:
            data[param] = 'qwerty'
        response4 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=data
        )
        Assertions.assert_code_status(response4, 400)
        Assertions.assert_json_has_key(response4, "error")
        assert response4.content.decode(
            'utf-8') == '{"error":"This user can only edit their own data."}', f"Unexpected content {response4.content}"

    @allure.description(
        "The test verifies that it is not possible to replace an email with an invalid one"
    )
    @allure.tag("Edit", "Negative", "Email")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
    def test_edit_this_user_email_to_incorrect_one(self):
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
        assert response2.content.decode(
            'utf-8') == '{"error":"Invalid email format"}', f"Unexpected content {response2.content}"

    @allure.description(
        "The test checks that it is not possible to replace the username with a very short name"
    )
    @allure.tag("Edit", "Negative", "Short name")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
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
        assert response2.content.decode(
            'utf-8') == '{"error":"The value for field `firstName` is too short"}', f"Unexpected content {response2.content}"
