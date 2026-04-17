from django.contrib.auth.models import Group
from users.models import User
from django.test import TestCase
from django.urls import reverse

from services.models import Service


class ServiceListViewTestCase(TestCase):
    """Тесты для проверки CRUD Услуг и прав доступа."""
    fixtures = ['roles.json']

    @classmethod
    def setUpTestData(cls):
        cls.marketer = User.objects.create_user(username='test-marketer', password='test123')
        cls.operator = User.objects.create_user(username='test-operator', password='test123')

        cls.marketer.groups.add(Group.objects.get(name='Маркетологи'))
        cls.operator.groups.add(Group.objects.get(name='Операторы'))

        cls.service = Service.objects.create(
            name='Тестовая Услуга',
            description='Описание',
            price=1000
        )

    def test_redirect_if_not_logged_in(self):
        """Гость не может смотреть список"""
        response = self.client.get(reverse('services:list'))
        self.assertRedirects(response, '/login/?next=/services/')

    def test_groups_perm(self):
        """Проверка наличия Групп и Прав"""
        self.client.login(username='test-operator', password='test123')
        oper_group_names = list(self.operator.groups.values_list('name', flat=True))
        market_group_names = list(self.marketer.groups.values_list('name', flat=True))

        self.assertIn('Операторы', oper_group_names)
        self.assertIn('Маркетологи', market_group_names)

        oper_perm = list(self.operator.get_all_permissions())
        market_perm = list(self.marketer.get_all_permissions())

        self.assertIn('leads.view_lead', oper_perm)
        self.assertEqual(len(oper_perm), 4)

        self.assertIn('services.change_service', market_perm)
        self.assertEqual(len(market_perm), 8)



    def test_forbidden_for_operator(self):
        """Оператор (без прав) получает, 302"""
        self.client.login(username='operator', password='test123')
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 302)

    def test_access_for_marketer(self):
        """Маркетолог (с правами) видит страницу, 200"""
        self.client.login(username='test-marketer', password='test123')
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_displays_service_name(self):
        """Проверяем, наличие в шаблоне"""
        self.client.login(username='test-marketer', password='test123')
        response = self.client.get(reverse('services:list'))
        self.assertContains(response, 'Тестовая Услуга')
        self.assertTemplateUsed(response, 'services/service-list.html')

    def test_create_view_service(self):
        """Проверяем создание услуги"""
        self.client.login(username='test-marketer', password='test123')
        count_before = Service.objects.count()

        response = self.client.post(reverse('services:create'), {
            'name': 'Новая Тестовая Услуга',
            'description': 'Детали',
            'price': '500.00'
        })

        self.assertRedirects(response, reverse('services:list'))
        self.assertEqual(Service.objects.count(), count_before + 1)
        self.assertTrue(Service.objects.filter(name='Новая Тестовая Услуга').exists())

    def test_update_view_service(self):
        """Проверяем редактирование услуги"""
        self.client.login(username='test-marketer', password='test123')
        service = Service.objects.create(name='Старая', price=100)

        response = self.client.post(
            reverse('services:update', kwargs={'pk': service.pk}),
            {'name': 'Обновлённая', 'description': 'Новое', 'price': '200.00'}
        )

        service.refresh_from_db()
        self.assertRedirects(response, reverse('services:list'))
        self.assertEqual(service.name, 'Обновлённая')

    def test_delete_view_service(self):
        """Проверяем удаление услуги"""
        self.client.login(username='test-marketer', password='test123')
        service = Service.objects.create(name='Удаляемая', price=100)
        count_before = Service.objects.count()

        response = self.client.post(reverse('services:delete', kwargs={'pk': service.pk}))

        self.assertRedirects(response, reverse('services:list'))
        self.assertEqual(Service.objects.count(), count_before - 1)
        self.assertFalse(Service.objects.filter(pk=service.pk).exists())
