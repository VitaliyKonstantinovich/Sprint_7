import pytest
import requests
import allure
import configuration
import helpers

class TestCourierDelete:

    @allure.title("Успешное удаление курьера")
    @allure.description("Проверяем, что существующий курьер успешно удаляется по его ID")
    def test_courier_delete_success(self):
        # 1. Создаем курьера (без фикстуры, т.к. нам нужно его удалить внутри теста)
        courier_payload = helpers.register_new_courier_and_return_login_password()
        
        # 2. Логинимся, чтобы получить его ID
        login_response = requests.post(configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH, json=courier_payload)
        courier_id = login_response.json().get("id")

        # 3. Отправляем запрос на удаление
        delete_response = requests.delete(f"{configuration.URL_SERVICE}{configuration.CREATE_COURIER_PATH}/{courier_id}")

        # проверяем статус 200 и текст {ok: true}
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title("Удаление курьера без передачи ID")
    @allure.description("Проверяем ошибку при попытке удалить курьера без ID")
    def test_courier_delete_without_id(self):
        # отправляем запрос на удаление, но не добавляем ID в конец пути
        response = requests.delete(configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH + "/")

        # проверяем ошибку 404 и текст (согласно документации API)
        assert response.status_code == 404
        assert response.json()["message"] == "Not Found."

    @allure.title("Удаление курьера с несуществующим ID")
    @allure.description("Проверяем ошибку при попытке удалить курьера с выдуманным ID")
    def test_courier_delete_with_non_existent_id(self):
        # придумываем несуществующий ID (например, очень большое число)
        non_existent_id = 999999999

        # отправляем запрос
        response = requests.delete(f"{configuration.URL_SERVICE}{configuration.CREATE_COURIER_PATH}/{non_existent_id}")

        # проверяем ошибку 404 и текст
        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет."
