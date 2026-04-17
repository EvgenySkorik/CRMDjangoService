from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from campaigns.models import Campaign
from leads.models import Lead
from services.models import Service
from users.models import User


class LeadListViewTestCase(TestCase):
    """Тесты для проверки CRUD Потенциального клиента и прав доступа."""
    fixtures = ['roles.json']

    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create_user(username='test-manager', password='test123')
        cls.operator = User.objects.create_user(username='test-operator', password='test123')

        cls.manager.groups.add(Group.objects.get(name='Менеджеры'))
        cls.operator.groups.add(Group.objects.get(name='Операторы'))

        cls.service = Service.objects.create(
            name='Тестовая Услуга',
            description='...',
            price=1000
        )
        cls.campaign = Campaign.objects.create(
            name='Тестовая Кампания',
            service=cls.service,
            channel='vk',
            budget=5000
        )

        cls.lead = Lead.objects.create(
            first_name='Тестовый',
            last_name='Клиент',
            middle_name='Потенциальный',
            telephone='84953552424',
            email='lid@lid.ru',
            campaign=cls.campaign,
        )

    def test_redirect_if_not_logged_in(self):
        """Гость не может смотреть список"""
        response = self.client.get(reverse('leads:list'))
        self.assertRedirects(response, '/login/?next=/leads/')

    def test_groups_perm(self):
        """Проверка наличия Групп и Прав"""

        manager_group_names = list(self.manager.groups.values_list('name', flat=True))

        self.assertIn('Менеджеры', manager_group_names)

        manager_perm = list(self.manager.get_all_permissions())
        oper_perm = list(self.operator.get_all_permissions())

        self.assertIn('leads.view_lead', manager_perm)
        self.assertIn('leads.add_lead', oper_perm)
        self.assertNotIn('leads.add_lead', manager_perm)
        self.assertEqual(len(manager_perm), 9)

    def test_access_for_manager(self):
        """Менеджер (с правами) видит страницу, 200"""
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('leads:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_displays_lead_name(self):
        """Проверяем, наличие в шаблоне"""
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('leads:list'))

        self.assertContains(response, 'Клиент Тестовый')
        self.assertTemplateUsed(response, 'leads/leads-list.html')

    def test_create_view_lead(self):
        """Проверяем создание лида с привязкой к кампании"""
        self.client.login(username='test-operator', password='test123')
        count_before = Lead.objects.count()

        response = self.client.post(reverse('leads:create'), {
            'first_name': 'НОВЫЙ',
            'last_name': 'Клиент',
            'middle_name': 'Тестовый',
            'telephone': '84953552424',
            'email': 'new@lid.ru',
            'campaign': self.campaign.pk,
        })

        self.assertRedirects(response, reverse('leads:list'))
        self.assertEqual(Lead.objects.count(), count_before + 1)

        new_lead = Lead.objects.get(first_name='НОВЫЙ')
        self.assertEqual(new_lead.campaign, self.campaign)

    def test_manager_cannot_update_lead(self):
        """Проверяем отказ менеджеру на редактирование лида"""
        self.client.login(username='test-manager', password='test123')

        response = self.client.post(
            reverse('leads:update', kwargs={'pk': self.lead.pk}),
            {'first_name': 'Обновлённая', }
        )

        self.assertEqual(response.status_code, 403)

    def test_operator_can_update_lead(self):
        """Оператор может редактировать лида"""
        self.client.login(username='test-operator', password='test123')

        response = self.client.post(
            reverse('leads:update', kwargs={'pk': self.lead.pk}),
            {'first_name': 'Обновлённая', 'last_name': 'Фамилия', 'telephone': '123', 'email': 'a@b.ru'}
        )

        self.assertRedirects(response, reverse('leads:list'))
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.first_name, 'Обновлённая')

    def test_lead_campaign_relation(self):
        """Проверяем, что лид правильно связан с кампанией"""
        self.client.login(username='test-operator', password='test123')
        self.assertEqual(self.lead.campaign, self.campaign)
        self.assertEqual(self.lead.campaign.name, 'Тестовая Кампания')
        self.assertIn(self.lead, self.campaign.leads.all())
