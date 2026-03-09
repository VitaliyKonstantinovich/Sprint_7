import requests
import allure
import configuration
import data


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    @allure.description("Проверяем, что курьер может принять заказ")
    def test_accept_order_success(self, courier_data, order_track):
        with allure.step("Подготовить данные для логина курьера"):
            login_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }

        with allure.step("Получить id курьера"):
            login_response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=login_payload
            )
            courier_id = login_response.json().get("id")

        with allure.step("Получить id заказа по треку"):
            track_params = {"t": order_track}
            order_response = requests.get(
                configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
                params=track_params
            )
            order_id = order_response.json()["order"]["id"]

        with allure.step("Принять заказ"):
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
        with allure.step("Получить id заказа по треку"):
            track_params = {"t": order_track}
            order_response = requests.get(
                configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
                params=track_params
            )
            order_id = order_response.json()["order"]["id"]

        with allure.step("Отправить запрос без courierId"):
            accept_response = requests.put(
                f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}"
            )

        assert accept_response.status_code == 400
        assert accept_response.json()["message"] == data.MESSAGE_NOT_ENOUGH_DATA

    @allure.title("Принятие заказа с неверным id курьера")
    @allure.description("Проверяем ошибку при попытке принять заказ с несуществующим id курьера")
    def test_accept_order_with_invalid_courier_id_returns_error(self, order_track):
        with allure.step("Получить id заказа по треку"):
            track_params = {"t": order_track}
            order_response = requests.get(
                configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH,
                params=track_params
            )
            order_id = order_response.json()["order"]["id"]

        with allure.step("Отправить запрос с несуществующим courierId"):
            params = {"courierId": data.INVALID_COURIER_ID}
            accept_response = requests.put(
                f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{order_id}",
                params=params
            )

        assert accept_response.status_code == 404
        assert accept_response.json()["message"] == data.MESSAGE_COURIER_NOT_FOUND

    @allure.title("Принятие заказа без id заказа")
    @allure.description("Проверяем ошибку при попытке принять заказ без id заказа")
    def test_accept_order_without_order_id_returns_error(self, courier_data):
        with allure.step("Подготовить данные для логина курьера"):
            login_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }

        with allure.step("Получить id курьера"):
            login_response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=login_payload
            )
            courier_id = login_response.json().get("id")

        with allure.step("Отправить запрос без id заказа"):
            params = {"courierId": courier_id}
            accept_response = requests.put(
                configuration.URL_SERVICE + configuration.ACCEPT_ORDER_PATH,
                params=params
            )

        assert accept_response.status_code == 404

    @allure.title("Принятие заказа с неверным id заказа")
    @allure.description("Проверяем ошибку при попытке принять заказ с несуществующим id заказа")
    def test_accept_order_with_invalid_order_id_returns_error(self, courier_data):
        with allure.step("Подготовить данные для логина курьера"):
            login_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }

        with allure.step("Получить id курьера"):
            login_response = requests.post(
                configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH,
                json=login_payload
            )
            courier_id = login_response.json().get("id")

        with allure.step("Отправить запрос с несуществующим id заказа"):
            params = {"courierId": courier_id}
            accept_response = requests.put(
                f"{configuration.URL_SERVICE}{configuration.ACCEPT_ORDER_PATH}{data.INVALID_ORDER_ID}",
                params=params
            )

        assert accept_response.status_code == 404
        assert accept_response.json()["message"] == data.MESSAGE_ORDER_NOT_FOUND