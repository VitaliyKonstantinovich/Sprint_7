import requests
import allure
import configuration
import helpers

class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    @allure.description("Проверяем, что курьер может принять заказ")
    def test_accept_order_success(self, courier_data, order_track):
        # 1. Получаем ID курьера
        login_response = requests.post(configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH, json=courier_data)
        courier_id = login_response.json().get("id")

        # 2. Получаем ID заказа по его трек-номеру (для принятия нужен ID, а не трек!)
        track_params = {"t": order_track}
        order_response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH, params=track_params)
        order_id = order_response.json()["order"]["id"]

        # 3. Принимаем заказ (передаем courierId в параметрах, как просили в задании)
        params = {"courierId": courier_id}
        accept_response = requests.put(f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}", params=params)

        # проверяем успешный статус 200
        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

    @allure.title("Принятие заказа без ID курьера")
    @allure.description("Проверяем ошибку при попытке принять заказ, не передав ID курьера")
    def test_accept_order_without_courier_id(self, order_track):
        # 1. Получаем ID заказа
        track_params = {"t": order_track}
        order_response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH, params=track_params)
        order_id = order_response.json()["order"]["id"]

        # 2. Пытаемся принять заказ без параметров курьера
        accept_response = requests.put(f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}")

        # проверяем ошибку 400
        assert accept_response.status_code == 400
        assert accept_response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Принятие заказа с неверным ID курьера")
    @allure.description("Проверяем ошибку при попытке принять заказ с несуществующим ID курьера")
    def test_accept_order_with_invalid_courier_id(self, order_track):
        # 1. Получаем ID заказа
        track_params = {"t": order_track}
        order_response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH, params=track_params)
        order_id = order_response.json()["order"]["id"]

        # 2. Пытаемся принять заказ с выдуманным ID курьера
        params = {"courierId": 999999999}
        accept_response = requests.put(f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}", params=params)

        # проверяем ошибку 404
        assert accept_response.status_code == 404
        assert accept_response.json()["message"] == "Курьера с таким id не существует"
