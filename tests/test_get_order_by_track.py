import requests
import allure
import configuration

class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по номеру трека")
    @allure.description("Проверяем, что запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self, order_track):
        # готовим параметры запроса (передаем трек)
        params = {"t": order_track}

        # отправляем GET запрос
        response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH, params=params)

        # проверяем статус 200
        assert response.status_code == 200
        # проверяем, что в ответе есть объект order
        assert "order" in response.json()

    @allure.title("Получение заказа без номера трека")
    @allure.description("Проверяем ошибку при запросе заказа без передачи трека")
    def test_get_order_without_track(self):
        # отправляем GET запрос вообще без параметров
        response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH)

        # проверяем ошибку 400
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Получение заказа с несуществующим номером трека")
    @allure.description("Проверяем ошибку при запросе заказа с выдуманным треком")
    def test_get_order_with_invalid_track(self):
        # выдумываем трек
        invalid_track = 999999999
        params = {"t": invalid_track}

        # отправляем запрос
        response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_BY_TRACK_PATH, params=params)

        # проверяем ошибку 404
        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"
