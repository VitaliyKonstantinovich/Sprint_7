import pytest
import requests
import allure
import configuration
import helpers

class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверяем, что при передаче всех обязательных полей курьер создается")
    def test_courier_creation_success(self):
        # готовим данные
        login = helpers.generate_random_string(10)
        password = helpers.generate_random_string(10)
        first_name = helpers.generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на создание
        response = requests.post(configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH, json=payload)

        # проверяем успешный статус код 201
        assert response.status_code == 201
        # проверяем, что в теле ответа ok: true
        assert response.json() == {"ok": True}

    @allure.title("Создание курьера с дублирующимся логином")
    @allure.description("Проверяем ошибку при попытке создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self):
        # готовим данные
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }

        # создаем первого курьера
        requests.post(configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH, json=payload)
        # пытаемся создать второго с такими же данными
        response = requests.post(configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH, json=payload)

        # проверяем код ошибки 409 (конфликт)
        assert response.status_code == 409
        # проверяем текст ошибки
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Создание курьера без обязательных полей")
    @allure.description("Параметризованный тест: проверяем ошибку при отсутствии логина или пароля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_creation_missing_required_fields(self, missing_field):
        # готовим полные данные
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        # удаляем одно поле в зависимости от параметра
        del payload[missing_field]

        # отправляем запрос
        response = requests.post(configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH, json=payload)

        # проверяем код ошибки 400 (Bad Request)
        assert response.status_code == 400
        # проверяем текст ошибки
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
