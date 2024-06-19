import requests
import time


class TestHeaders:
    def test_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        # Запрос для печати headers в тесте
        response1 = requests.get(url)
        expected_headers = dict(response1.headers)
        print(expected_headers)

        # Выполнение следующего запроса без ожидания, до истечения срока действия headers
        response2 = requests.get(url)
        headers_value2 = response2.headers
        assert response2.status_code == 200, "Wrong response code."
        assert expected_headers == headers_value2, "The headers have expired."

        # Выполнение следующего запроса с ожиданием, для проверки изменения headers
        time.sleep(3)
        response3 = requests.get(url)
        headers_value3 = response3.headers
        assert response3.status_code == 200, "Wrong response code."
        assert expected_headers != headers_value3, "The headers received is not changed."
