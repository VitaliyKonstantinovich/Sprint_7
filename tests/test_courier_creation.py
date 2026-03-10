import allure
import pytest
import requests

import configuration
import data
import helpers


class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверяем, что при передаче всех обязательных полей курьер создается")
    def test_courier_creation_success(self):
        # готовим данные
        with allure.step("Подготовить данные для создания курьера"):
            payload = {
                "login": helpers.generate_random_string(10),
                "password": helpers.generate_random_string(10),
                "firstName": helpers.generate_random_string(10)
            }

        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH,
                json=payload
            )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Создание курьера с дублирующимся логином")
    @allure.description("Проверяем ошибку при попытке создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self):
        with allure.step("Подготовить данные для создания курьера"):
            payload = {
                "login": helpers.generate_random_string(10),
                "password": helpers.generate_random_string(10),
                "firstName": helpers.generate_random_string(10)
            }

        with allure.step("Отправить первый запрос на создание курьера"):
            requests.post(
                configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH,
                json=payload
            )

        with allure.step("Отправить второй запрос на создание такого же курьера"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH,
                json=payload
            )

        assert response.status_code == 409
        assert response.json()["message"] == data.MESSAGE_LOGIN_ALREADY_USED

    @allure.title("Создание курьера без обязательных полей")
    @allure.description("Параметризованный тест: проверяем ошибку при отсутствии логина или пароля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_creation_missing_required_fields(self, missing_field):
        with allure.step("Подготовить полные данные для создания курьера"):
            payload = {
                "login": helpers.generate_random_string(10),
                "password": helpers.generate_random_string(10),
                "firstName": helpers.generate_random_string(10)
            }

        with allure.step("Удалить обязательное поле из payload"):
            del payload[missing_field]

        with allure.step("Отправить запрос на создание курьера без обязательного поля"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH,
                json=payload
            )

        assert response.status_code == 400
        assert response.json()["message"] == data.MESSAGE_NOT_ENOUGH_DATA_FOR_COURIER