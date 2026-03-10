import allure
import pytest
import requests

import configuration
import data


class TestOrderCreation:

    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description("Параметризованный тест: проверяем создание заказа с цветом BLACK, GREY, обоими или без цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_order_creation_with_different_colors(self, color):
        with allure.step("Подготовить тело запроса для создания заказа"):
            current_body = data.order_body.copy()
            current_body["color"] = color

        with allure.step("Отправить запрос на создание заказа"):
            response = requests.post(
                configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH,
                json=current_body
            )

        assert response.status_code == 201
        assert "track" in response.json()