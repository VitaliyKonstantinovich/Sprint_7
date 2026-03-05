import pytest
import requests
import allure
import configuration

class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверяем, что курьер может войти с правильным логином и паролем, возвращается id")
    def test_courier_login_success(self, courier_data):
        # берем данные созданного курьера из фикстуры
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        # отправляем запрос на вход
        response = requests.post(configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH, json=login_payload)

        # проверяем успешный статус код 200
        assert response.status_code == 200
        # проверяем, что вернулся id курьера
        assert "id" in response.json()

    @allure.title("Авторизация с неверными данными или пустыми полями")
    @allure.description("Параметризованный тест: проверяем ошибки при неверном логине/пароле или их отсутствии")
    @pytest.mark.parametrize("payload", [
        {"login": "non_existent_login", "password": "non_existent_password"}, # полностью неверные данные
        {"login": "non_existent_login", "password": ""}, # пустой пароль
        {"login": "", "password": "non_existent_password"}  # пустой логин
    ])
    def test_login_with_invalid_credentials_or_missing_fields(self, payload):
        # отправляем запрос с проблемными данными
        response = requests.post(configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH, json=payload)

        # проверяем, что вернулась ошибка 400 или 404
        assert response.status_code in [400, 404]
        
        # проверяем текст ошибки в зависимости от кода
        if response.status_code == 400:
            assert response.json()["message"] == "Недостаточно данных для входа"
        else:
            assert response.json()["message"] == "Учетная запись не найдена"
