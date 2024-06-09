import requests

# 1. Делает http-запрос любого типа без параметра method.
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

# 2. Делает http-запрос не из списка. Например, HEAD.
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print(response.text)

# 3. Делает запрос с правильным значением method.
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response.text)

response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "PUT"})
print(response.text)

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
types = ["post", "get", "put", "delete"]
methods = ["POST", "GET", "PUT", "DELETE"]

for i in types:
    for j in methods:
        if i == "get":
            response = requests.get(url=url, params={"method": j})
            print(response.text)
        else:
            response = requests.request(i, url=url, data={"method": j})
            print(response.text)
