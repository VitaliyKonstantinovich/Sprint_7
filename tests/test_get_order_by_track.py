import allure
import requests

import configuration
import data


class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по номеру трека")
    @allure.description("Проверяем, что запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self, order_track):
        with allure.step("Подготовить параметры запроса с номером трека"):
            params = {"t": order_track}

        with allure.step("Отправить запрос на получение заказа по треку"):
            response = requests.get(
                configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
                params=params
            )

        assert response.status_code == 200
        assert "order" in response.json()

    @allure.title("Получение заказа без номера трека")
    @allure.description("Проверяем ошибку при запросе заказа без передачи трека")
    def test_get_order_without_track(self):
        with allure.step("Отправить запрос на получение заказа без трека"):
            response = requests.get(
                configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH
            )

        assert response.status_code == 400
        assert response.json()["message"] == data.MESSAGE_NOT_ENOUGH_DATA

    @allure.title("Получение заказа с несуществующим номером трека")
    @allure.description("Проверяем ошибку при запросе заказа с выдуманным треком")
    def test_get_order_with_invalid_track(self):
        with allure.step("Подготовить параметры запроса с несуществующим треком"):
            params = {"t": data.INVALID_TRACK}

        with allure.step("Отправить запрос на получение заказа с неверным треком"):
            response = requests.get(
                configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
                params=params
            )

        assert response.status_code == 404
        assert response.json()["message"] == data.MESSAGE_ORDER_BY_TRACK_NOT_FOUND