# CRM Система на Django

## Стек
- Django 6.0
- PostgreSQL 15 (Docker)
- uv
- Pylint, Mypy

## Установка
1. ```bash
   git clone https://github.com/EvgenySkorik/CRMDjangoService.git
   cd CRMDjangoService
   ```
2. ```bash
    cp .env.example .env
   ```

3. ```bash
    docker compose up -d --build`
   ```
4. ```bash
    docker exec -it crm_web uv run python manage.py createsuperuser`
   ```
5. http://localhost:8000


## Функционал
- CRUD для услуг, кампаний, лидов, контрактов, клиентов
- Роли: Маркетолог, Оператор, Менеджер
- Статистика
- PostgreSQL
- Unit-тесты

## Тесты
`python manage.py test`

## Pylint/MyPy
- `pylint .`
- `mypy .`