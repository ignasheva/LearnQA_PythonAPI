import requests
import time

URL = "https://playground.learnqa.ru/ajax/api/longtime_job"


def status_func(status):
    message = ""
    response = requests.get(f"{URL}?token={token}")
    obj = response.json()
    if obj["status"] == status:
        message = f"This is a correct status. {status}."
    if "result" in obj:
        message += " The 'result' field exists"
    return message


task_response = requests.get(url=URL)
task_obj = task_response.json()
token, seconds = task_obj["token"], task_obj["seconds"]
print(status_func("Job is NOT ready"))
time.sleep(seconds)
print(status_func("Job is ready"))
