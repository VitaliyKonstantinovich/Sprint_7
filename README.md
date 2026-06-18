# API автотесты Яндекс Самокат

Проект содержит API-автотесты для сервиса «Яндекс Самокат».
Тесты написаны на Python с использованием Pytest, Requests и Allure.

## Цель проекта

Проверить ключевые API-сценарии сервиса:

* создание курьера;
* авторизацию курьера;
* создание заказа;
* получение заказа по трек-номеру;
* получение списка заказов;
* принятие заказа;
* удаление курьера.

## Что проверяется

### Курьер

* успешное создание курьера;
* невозможность создать двух одинаковых курьеров;
* ошибка при создании курьера без обязательных полей;
* успешный логин курьера;
* ошибки при логине с некорректными или неполными данными;
* удаление курьера.

### Заказ

* создание заказа с разными вариантами выбора цвета;
* создание заказа без выбора цвета;
* получение заказа по трек-номеру;
* получение списка заказов;
* принятие заказа курьером.

## Стек

* Python
* Pytest
* Requests
* Allure
* Git

## Структура проекта

```text
Sprint_7/
├── configuration.py
├── data.py
├── helpers.py
├── requirements.txt
├── README.md
└── tests/
    ├── conftest.py
    ├── test_accept_order.py
    ├── test_courier_creation.py
    ├── test_courier_delete.py
    ├── test_courier_login.py
    ├── test_get_order_by_track.py
    ├── test_get_orders_list.py
    └── test_order_creation.py
```

## Как запустить проект

### 1. Клонировать репозиторий

```bash
git clone https://github.com/VitaliyKonstantinovich/Sprint_7.git
cd Sprint_7
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
```

### 3. Активировать виртуальное окружение

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Если PowerShell блокирует запуск скриптов:

```bash
venv\Scripts\activate.bat
```

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

### 5. Запустить тесты

```bash
pytest tests
```

### 6. Запустить тесты с генерацией Allure-результатов

```bash
pytest tests --alluredir=allure_results
```

### 7. Открыть Allure-отчёт

```bash
allure serve allure_results
```

## Результат

В проекте подготовлен набор API-автотестов, который проверяет основные backend-сценарии сервиса «Яндекс Самокат»: работу с курьерами, заказами, авторизацией и получением данных.

Локальная проверка проекта: 25 тестов прошли успешно.

## Автор

Vitaliy Glebov
QA Engineer | Manual Testing | API | SQL | Python / Pytest
