import requests
import allure
import configuration


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    @allure.description("Проверяем, что курьер может принять заказ")
    def test_accept_order_success(self, courier_data, order_track):
        # получаем id курьера
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        login_response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=login_payload
        )
        courier_id = login_response.json().get("id")

        # получаем id заказа по треку
        track_params = {"t": order_track}
        order_response = requests.get(
            configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
            params=track_params
        )
        order_id = order_response.json()["order"]["id"]

        # принимаем заказ
        params = {"courierId": courier_id}
        accept_response = requests.put(
            f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}",
            params=params
        )

        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

    @allure.title("Принятие заказа без id курьера")
    @allure.description("Проверяем ошибку при попытке принять заказ без id курьера")
    def test_accept_order_without_courier_id_returns_error(self, order_track):
        # получаем id заказа
        track_params = {"t": order_track}
        order_response = requests.get(
            configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
            params=track_params
        )
        order_id = order_response.json()["order"]["id"]

        # отправляем запрос без courierId
        accept_response = requests.put(
            f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}"
        )

        assert accept_response.status_code == 400
        assert accept_response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Принятие заказа с неверным id курьера")
    @allure.description("Проверяем ошибку при попытке принять заказ с несуществующим id курьера")
    def test_accept_order_with_invalid_courier_id_returns_error(self, order_track):
        # получаем id заказа
        track_params = {"t": order_track}
        order_response = requests.get(
            configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
            params=track_params
        )
        order_id = order_response.json()["order"]["id"]

        # отправляем запрос с несуществующим courierId
        params = {"courierId": 999999999}
        accept_response = requests.put(
            f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}",
            params=params
        )

        assert accept_response.status_code == 404
        assert accept_response.json()["message"] == "Курьера с таким id не существует"

    @allure.title("Принятие заказа без id заказа")
    @allure.description("Проверяем ошибку при попытке принять заказ без id заказа")
    def test_accept_order_without_order_id_returns_error(self, courier_data):
        # получаем id курьера
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        login_response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=login_payload
        )
        courier_id = login_response.json().get("id")

        # отправляем запрос без id заказа
        params = {"courierId": courier_id}
        accept_response = requests.put(
            configuration.URL_SERVICE + configuration.ACCEPT_ORDER_PATH,
            params=params
        )

        assert accept_response.status_code == 404

    @allure.title("Принятие заказа с неверным id заказа")
    @allure.description("Проверяем ошибку при попытке принять заказ с несуществующим id заказа")
    def test_accept_order_with_invalid_order_id_returns_error(self, courier_data):
        # получаем id курьера
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        login_response = requests.post(
            configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
            json=login_payload
        )
        courier_id = login_response.json().get("id")

        # отправляем запрос с несуществующим id заказа
        params = {"courierId": courier_id}
        invalid_order_id = 999999999
        accept_response = requests.put(
            f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{invalid_order_id}",
            params=params
        )

        assert accept_response.status_code == 404
        assert accept_response.json()["message"] == "Заказа с таким id не существует"