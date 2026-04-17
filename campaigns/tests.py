from django.contrib.auth.models import Group

from campaigns.models import Campaign
from users.models import User
from django.test import TestCase
from django.urls import reverse

from services.models import Service


class CampaignListViewTestCase(TestCase):
    """Тесты для проверки CRUD Рекламных компаний и прав доступа."""
    fixtures = ['roles.json']

    @classmethod
    def setUpTestData(cls):
        cls.marketer = User.objects.create_user(username='test-marketer', password='test123')
        cls.manager = User.objects.create_user(username='test-manager', password='test123')

        cls.marketer.groups.add(Group.objects.get(name='Маркетологи'))
        cls.manager.groups.add(Group.objects.get(name='Менеджеры'))

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

    def test_redirect_if_not_logged_in(self):
        """Гость не может смотреть список"""
        response = self.client.get(reverse('campaigns:list'))
        self.assertRedirects(response, '/login/?next=/campaigns/')

    def test_forbidden_for_manager(self):
        """Менеджер (без прав на кампании) получает 403"""
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('campaigns:list'))
        self.assertEqual(response.status_code, 403)

    def test_access_for_marketer(self):
        """Маркетолог (с правами) видит страницу, 200"""
        self.client.login(username='test-marketer', password='test123')
        response = self.client.get(reverse('campaigns:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_displays_campaign_name(self):
        """Проверяем, наличие в шаблоне"""
        self.client.login(username='test-marketer', password='test123')
        response = self.client.get(reverse('campaigns:list'))
        self.assertContains(response, 'Тестовая Кампания')
        self.assertTemplateUsed(response, 'campaigns/campaign-list.html')

    def test_create_view_campaign(self):
        """Проверяем создание услуги"""
        self.client.login(username='test-marketer', password='test123')
        count_before = Campaign.objects.count()

        response = self.client.post(reverse('campaigns:create'), {
            'name': 'НОВАЯ КОМПАНИЯ',
            'service': self.service.pk,
            'channel': 'vk',
            'budget': 8000,
        })

        self.assertRedirects(response, reverse('campaigns:list'))
        self.assertEqual(Campaign.objects.count(), count_before + 1)
        self.assertTrue(Campaign.objects.filter(name='НОВАЯ КОМПАНИЯ').exists())


    def test_delete_view_campaign(self):
        """Проверяем удаление компании"""
        self.client.login(username='test-marketer', password='test123')
        campaign = Campaign.objects.create(name='Удаляемая', service=self.service, channel='vk', budget=2000)
        count_before = Campaign.objects.count()

        response = self.client.post(reverse('campaigns:delete', kwargs={'pk': campaign.pk}))

        self.assertRedirects(response, reverse('campaigns:list'))
        self.assertEqual(Campaign.objects.count(), count_before - 1)
        self.assertFalse(Campaign.objects.filter(pk=campaign.pk).exists())
