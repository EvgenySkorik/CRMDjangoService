# CRM Система на Django

## Стек
- Django 6.0
- PostgreSQL 15 (Docker)
- uv
- Pylint, Mypy

## Установка
1. ```bash
   git clone https://github.com/EvgenySkorik/CRM-Django.git
   cd CRM-Django
   ```
2. `cp .env.example .env`

3.`docker compose up -d --build`
4.`docker exec -it crm_web uv run python manage.py createsuperuser`
5. `http://localhost:8000`


## Функционал
- CRUD для услуг, кампаний, лидов, контрактов, клиентов
- Роли: Маркетолог, Оператор, Менеджер
- Статистика
- PostgreSQL
- Unit-тесты

## Тесты
`python manage.py test`

## Pylint/MyPy
`pylint .`
`mypy .`