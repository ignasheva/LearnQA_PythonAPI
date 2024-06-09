import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(json_text)
key1, key2, index = "messages", "message", 1
if key1 in obj:
    obj = obj[key1][index]
    if key2 in obj:
        obj = obj[key2]
        print(obj)
    else:
        print(f"Ключа {key2} в JSON нет.")
else:
    print(f"Ключа {key1} в JSON нет.")
