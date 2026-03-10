import allure
import requests

import configuration
import data


class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверяем, что курьер может войти с правильным логином и паролем")
    def test_courier_login_with_valid_data_returns_id(self, courier_data):
        with allure.step("Подготовить тело запроса для авторизации курьера"):
            payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }

        with allure.step("Отправить запрос на авторизацию курьера"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=payload
            )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Авторизация без логина")
    @allure.description("Проверяем ошибку при попытке авторизации без логина")
    def test_courier_login_without_login_returns_error(self, courier_data):
        with allure.step("Подготовить тело запроса без логина"):
            payload = {
                "password": courier_data["password"]
            }

        with allure.step("Отправить запрос на авторизацию без логина"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=payload
            )

        assert response.status_code in [400, 504]

    @allure.title("Авторизация без пароля")
    @allure.description("Проверяем ошибку при попытке авторизации без пароля")
    def test_courier_login_without_password_returns_error(self, courier_data):
        with allure.step("Подготовить тело запроса без пароля"):
            payload = {
                "login": courier_data["login"]
            }

        with allure.step("Отправить запрос на авторизацию без пароля"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=payload
            )

        assert response.status_code in [400, 504]

    @allure.title("Авторизация с неверным логином")
    @allure.description("Проверяем ошибку при попытке авторизации с неверным логином")
    def test_courier_login_with_invalid_login_returns_error(self, courier_data):
        with allure.step("Подготовить тело запроса с неверным логином"):
            payload = {
                "login": data.INVALID_LOGIN,
                "password": courier_data["password"]
            }

        with allure.step("Отправить запрос на авторизацию с неверным логином"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=payload
            )

        assert response.status_code == 404
        assert response.json()["message"] == data.MESSAGE_ACCOUNT_NOT_FOUND

    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверяем ошибку при попытке авторизации с неверным паролем")
    def test_courier_login_with_invalid_password_returns_error(self, courier_data):
        with allure.step("Подготовить тело запроса с неверным паролем"):
            payload = {
                "login": courier_data["login"],
                "password": data.INVALID_PASSWORD
            }

        with allure.step("Отправить запрос на авторизацию с неверным паролем"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=payload
            )

        assert response.status_code == 404
        assert response.json()["message"] == data.MESSAGE_ACCOUNT_NOT_FOUND