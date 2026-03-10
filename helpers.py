import random
import string

import allure
import requests

import configuration


@allure.step("Генерация случайной строки")
def generate_random_string(length):
    # генерируем строку из букв нижнего регистра
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


@allure.step("Подготовка данных для нового курьера")
def register_new_courier_and_return_login_password():
    # создаем уникальные логин, пароль и имя
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса в словарь
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем POST-запрос на создание курьера
    with allure.step("Отправить запрос на создание курьера"):
        response = requests.post(
            configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH,
            json=payload
        )

    # если курьер создался успешно, возвращаем его данные
    if response.status_code == 201:
        return payload

    return None