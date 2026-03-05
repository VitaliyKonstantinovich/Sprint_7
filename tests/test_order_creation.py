import pytest
import requests
import allure
import configuration
import data

class TestOrderCreation:
    
    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description("Параметризованный тест: проверяем создание заказа с цветом BLACK, GREY, обоими или без цвета")
    @pytest.mark.parametrize("color", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([]) # пустой массив означает отсутствие цвета
    ])
    def test_order_creation_with_different_colors(self, color):
        # берем шаблон тела заказа и создаем копию
        current_body = data.order_body.copy()
        # подставляем цвет из параметра
        current_body["color"] = color

        # отправляем запрос на создание заказа
        response = requests.post(configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH, json=current_body)

        # проверяем статус код 201
        assert response.status_code == 201
        # проверяем, что в ответе вернулся номер трека заказа
        assert "track" in response.json()
