import requests
import allure
import configuration


class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверяем, что курьер может войти с правильным логином и паролем")
    def test_courier_login_with_valid_data_returns_id(self, courier_data):
        # подготавливаем тело запроса
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        # отправляем запрос
        response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=payload
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Авторизация без логина")
    @allure.description("Проверяем ошибку при попытке авторизации без логина")
    def test_courier_login_without_login_returns_error(self, courier_data):
        # подготавливаем тело запроса без login
        payload = {
            "password": courier_data["password"]
        }

        # отправляем запрос
        response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=payload
        )

        assert response.status_code != 200

    @allure.title("Авторизация без пароля")
    @allure.description("Проверяем ошибку при попытке авторизации без пароля")
    def test_courier_login_without_password_returns_error(self, courier_data):
        # подготавливаем тело запроса без password
        payload = {
            "login": courier_data["login"]
        }

        # отправляем запрос
        response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=payload
        )

        assert response.status_code != 200

    @allure.title("Авторизация с неверным логином")
    @allure.description("Проверяем ошибку при попытке авторизации с неверным логином")
    def test_courier_login_with_invalid_login_returns_error(self, courier_data):
        # подготавливаем тело запроса
        payload = {
            "login": "wrong_login",
            "password": courier_data["password"]
        }

        # отправляем запрос
        response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=payload
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверяем ошибку при попытке авторизации с неверным паролем")
    def test_courier_login_with_invalid_password_returns_error(self, courier_data):
        # подготавливаем тело запроса
        payload = {
            "login": courier_data["login"],
            "password": "wrong_password"
        }

        # отправляем запрос
        response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=payload
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"