# API Client Generator


**API Client Generator** — это инструмент для автоматической генерации клиентского кода на основе Swagger (OpenAPI) спецификации. С его помощью можно генерировать:

- **Pydantic модели** для запросов (Request) и ответов (Response)
- **Клиентские классы** для вызова эндпоинтов API (с группировкой по тегам)
- **Локальный фасад** для объединения клиентских классов в единый интерфейс
- **Глобальный фасад** для работы с несколькими API клиентами

## Установка

Установите пакет со всеми зависимостями через `pip`:

```bash
pip install git+ssh://git@liis-it.gitlab.yandexcloud.net/inner/tests/api-client-generator.git@update-all
```

# Генерация случайных данных для Pydantic моделей

Этот модуль позволяет автоматически генерировать случайны данные для любых Pydantic-моделей.

**GenData**  
  Заполнения всех (или только обязательных/опциональных) полей Pydantic-модели и создания экземпляра модели без полной валидации.
```
# Заполнить только обязательные поля
instance = GenData(ApplicationResponse).fill_required().build()

# Заполнить только опциональные поля
instance = GenData(ApplicationResponse).fill_optional().build()

# Получить экземпляр модели со всеми заполненными полями
model_instance = GenData(ApplicationResponse).fill_all().build()

# Генерация всех полей модели и получение JSON
json_data = GenData(ApplicationResponse).fill_all().build().model_dump_json()

# Получить словарь
data_dict = GenData(ApplicationResponse).fill_all().build().model_dump()
```
## Как использовать
```bash
rest_gen --swagger-url <URL_к_Swagger_JSON>
```
### Структура, создаваемая в проекте
```
http_clients/
├── <service_name_1>/
│   ├── models.py        # Pydantic модели для запросов (Request) и ответов (Response)
│   ├── facade.py        # Локальный фасад, объединяющий клиентские классы сервиса
│   └── endpoints/       # Клиентские классы, сгенерированные по тегам
│        ├── <tag1>_client.py
│        ├── <tag2>_client.py
│        └── ...
├── <service_name_2>/
│   ├── models.py        
│   ├── facade.py        
│   └── endpoints/       
│        ├── <tag1>_client.py
│        ├── <tag2>_client.py
│        └── ...
└── api_facade.py        # Глобальный фасад, объединяющий локальные фасады сервисов
```
