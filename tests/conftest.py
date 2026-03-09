import pytest
import requests
import allure
import configuration
import helpers
import data


@pytest.fixture(scope='function')
def courier_data():
    with allure.step("Создать данные нового курьера"):
        courier = helpers.register_new_courier_and_return_login_password()

    yield courier

    with allure.step("Подготовить payload для логина курьера"):
        login_payload = {
            "login": courier["login"],
            "password": courier["password"]
        }

    with allure.step("Получить id курьера после выполнения теста"):
        login_response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=login_payload
        )
        courier_id = login_response.json().get("id")

    if courier_id:
        with allure.step("Удалить созданного курьера"):
            requests.delete(
                f"{configuration.URL_SERVICE}{configuration.CREATE_COURIER_PATH}/{courier_id}"
            )


@pytest.fixture(scope='function')
def order_track():
    with allure.step("Создать тестовый заказ"):
        response = requests.post(
            configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH,
            json=data.order_body
        )

    with allure.step("Получить номер трека заказа"):
        track_number = response.json().get("track")

    yield track_number