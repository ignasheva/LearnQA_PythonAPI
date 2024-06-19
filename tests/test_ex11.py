import requests
import time


class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        # Запрос для печати cookie в тесте. Сохранение данных в переменные
        response1 = requests.get(url)
        expected_cookie = dict(response1.cookies)
        print(expected_cookie)
        key = list(expected_cookie)[0]
        value = expected_cookie[key]

        # Основной запрос для проверок assert-ом
        time.sleep(3)
        response2 = requests.get(url)
        # Проверка получения успешного ответа на запрос
        assert response2.status_code == 200, "Wrong response code."
        response_cookie = response2.cookies
        # Проверка того, что ключ cookie не изменяется при следующем запросе
        assert key in response_cookie, f"There are no cookies with this key: {key} "
        # Проверка, что значение cookie не изменяется при следующем запросе
        assert response_cookie[key] == value, f"The cookie received is not {value} that you expected."
