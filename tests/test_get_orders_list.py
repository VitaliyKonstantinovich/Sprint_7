import requests
import allure
import configuration

class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что запрос возвращает непустой список заказов")
    def test_get_orders_list_returns_list(self):
        # отправляем GET запрос на получение заказов
        response = requests.get(configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH)

        # проверяем статус код 200
        assert response.status_code == 200
        # проверяем, что ключ orders содержит список (list)
        assert isinstance(response.json()["orders"], list)
