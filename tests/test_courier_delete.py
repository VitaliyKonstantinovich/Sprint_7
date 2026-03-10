import allure
import requests

import configuration
import data
import helpers


class TestCourierDelete:

    @allure.title("Успешное удаление курьера")
    @allure.description("Проверяем, что существующий курьер успешно удаляется по его ID")
    def test_courier_delete_success(self):
        with allure.step("Создать курьера"):
            courier_payload = helpers.register_new_courier_and_return_login_password()

        with allure.step("Отправить запрос на логин курьера"):
            login_response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=courier_payload
            )

        with allure.step("Получить id курьера"):
            courier_id = login_response.json().get("id")

        with allure.step("Отправить запрос на удаление курьера"):
            delete_response = requests.delete(
                f"{configuration.URL_SERVICE}{configuration.CREATE_COURIER_PATH}/{courier_id}"
            )

        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title("Удаление курьера без передачи ID")
    @allure.description("Проверяем ошибку при попытке удалить курьера без ID")
    def test_courier_delete_without_id(self):
        with allure.step("Отправить запрос на удаление курьера без id"):
            response = requests.delete(
                configuration.URL_SERVICE + configuration.CREATE_COURIER_PATH + "/"
            )

        assert response.status_code == 404
        assert response.json()["message"] == data.MESSAGE_NOT_FOUND

    @allure.title("Удаление курьера с несуществующим ID")
    @allure.description("Проверяем ошибку при попытке удалить курьера с выдуманным ID")
    def test_courier_delete_with_non_existent_id(self):
        with allure.step("Отправить запрос на удаление курьера с несуществующим id"):
            response = requests.delete(
                f"{configuration.URL_SERVICE}{configuration.CREATE_COURIER_PATH}/{data.INVALID_COURIER_ID}"
            )

        assert response.status_code == 404
        assert response.json()["message"] == data.MESSAGE_COURIER_ID_NOT_FOUND