import pytest
import requests
import configuration
import helpers
import data

@pytest.fixture(scope='function')
def courier_data():
    # создаем данные для нового курьера
    data = helpers.register_new_courier_and_return_login_password()

    # передаем данные в тест
    yield data

    # получаем id курьера после выполнения теста
    login_payload = {
        "login": data["login"],
        "password": data["password"]
    }
    login_response = requests.post(configuration.URL_SERVICE + configuration.LOGIN_COURIER_PATH, json=login_payload)
    courier_id = login_response.json().get("id")

    # если id получен, удаляем курьера
    if courier_id:
        requests.delete(f"{configuration.URL_SERVICE}{configuration.CREATE_COURIER_PATH}/{courier_id}")

# --- Добавлено для дополнительного задания ---
@pytest.fixture(scope='function')
def order_track():
    # отправляем запрос на создание тестового заказа
    response = requests.post(configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH, json=data.order_body)
    
    # извлекаем номер трека из ответа
    track_number = response.json().get("track")
    
    # передаем номер трека в тест
    yield track_number
    # (Очистка заказа не требуется, так как в API нет надежной ручки удаления/отмены заказа по треку)
