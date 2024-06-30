import allure
import time
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Delete cases")
class TestUserDelete(BaseCase):
    @allure.description("The test checks that it is impossible to edit a user with id=2")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
    def test_delete_user_with_id2(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=data
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            'utf-8') == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}', \
            f"Unexpected content {response2.content}"

    @allure.description("The test checks that it is possible to delete a newly created user")
    @allure.tag("Delete", "Positive")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=login_data
        )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode(
            'utf-8') == "User not found", f"Unexpected content {response4.content}"

    @allure.description("The test checks that it is impossible to delete a user while logged in as another user")
    @allure.tag("Delete", "Negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Irina Ignasheva")
    @allure.link("https://confa.com/", name="Link to documentation")
    def test_delete_user_auth_as_other_user(self):
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

        # DELETE USER 2
        response4 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4, 400)
        Assertions.assert_json_has_key(response4, "error")
        assert response4.content.decode(
            'utf-8') == '{"error":"This user can only delete their own account."}',\
            f"Unexpected content {response4.content}"
