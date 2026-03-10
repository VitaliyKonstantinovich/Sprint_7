import allure
import requests

import configuration


class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что запрос возвращает непустой список заказов")
    def test_get_orders_list_returns_list(self):
        with allure.step("Отправить запрос на получение списка заказов"):
            response = requests.get(
                configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH
            )

        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)