import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
# Количество редиректов
number_of_redirects = len(response.history)
print(number_of_redirects)
# Конечный URL
print(response.url)
