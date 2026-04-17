from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract
from services.models import Service
from users.models import User


class ContractListViewTestCase(TestCase):
    """Тесты для проверки CRUD Контрактов и прав доступа."""
    fixtures = ['roles.json']

    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create_user(username='test-manager', password='test123')
        cls.marketer = User.objects.create_user(username='test-marketer', password='test123')

        cls.manager.groups.add(Group.objects.get(name='Менеджеры'))
        cls.marketer.groups.add(Group.objects.get(name='Маркетологи'))

        cls.fake_file = SimpleUploadedFile(
            "contract.pdf",
            b"file_content",
            content_type="application/pdf"
        )

        cls.service = Service.objects.create(
            name='Тестовая Услуга',
            description='Описание',
            price=1000
        )

        cls.contract = Contract.objects.create(
            name='Тестовый Контракт',
            service=cls.service,
            start_date='2024-01-01',
            end_date='2024-12-31',
            amount=50000
        )

    def test_redirect_if_not_logged_in(self):
        """Гость не может смотреть список"""
        response = self.client.get(reverse('contracts:list'))
        self.assertRedirects(response, '/login/?next=/contracts/')

    def test_groups_perm(self):
        """Проверка наличия Групп и Прав"""
        manager_perms = list(self.manager.get_all_permissions())

        self.assertIn('contracts.view_contract', manager_perms)
        self.assertIn('contracts.add_contract', manager_perms)
        self.assertIn('contracts.change_contract', manager_perms)
        self.assertIn('contracts.delete_contract', manager_perms)

    def test_access_for_manager(self):
        """Менеджер (с правами) видит страницу, 200"""
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('contracts:list'))
        self.assertEqual(response.status_code, 200)

    def test_forbidden_for_marketer(self):
        """Маркетолог (без прав) получает 403"""
        self.client.login(username='test-marketer', password='test123')
        response = self.client.get(reverse('contracts:list'))
        self.assertEqual(response.status_code, 403)

    def test_list_view_displays_contract_name(self):
        """Проверяем наличие контракта в шаблоне"""
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('contracts:list'))
        self.assertContains(response, 'Тестовый Контракт')
        self.assertTemplateUsed(response, 'contracts/contracts-list.html')

    def test_create_view_contract(self):
        """Проверяем создание контракта"""
        self.client.login(username='test-manager', password='test123')
        count_before = Contract.objects.count()

        response = self.client.post(reverse('contracts:create'), {
            'name': 'НОВЫЙ Контракт',
            'service': self.service.pk,
            'start_date': '2024-06-01',
            'end_date': '2024-12-31',
            'amount': 75000,
            'document': self.fake_file,
        })

        self.assertRedirects(response, reverse('contracts:list'))
        self.assertEqual(Contract.objects.count(), count_before + 1)
        self.assertTrue(Contract.objects.filter(name='НОВЫЙ Контракт').exists())

    def test_manager_can_update_contract(self):
        """Менеджер может редактировать контракт"""
        self.client.login(username='test-manager', password='test123')

        response = self.client.post(
            reverse('contracts:update', kwargs={'pk': self.contract.pk}),
            {
                'name': 'Обновлённый Контракт',
                'service': self.service.pk,
                'start_date': '2024-01-01',
                'end_date': '2024-12-31',
                'amount': 90000,
                'document': self.fake_file,
            }
        )

        self.assertRedirects(response, reverse('contracts:list'))
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.name, 'Обновлённый Контракт')

    def test_marketer_cannot_update_contract(self):
        """Маркетолог не может редактировать контракт"""
        self.client.login(username='test-marketer', password='test123')

        response = self.client.post(
            reverse('contracts:update', kwargs={'pk': self.contract.pk}),
            {
                'name': 'Взлом',
                'service': self.service.pk,
                'start_date': '2024-01-01',
                'end_date': '2024-12-31',
                'amount': 1,
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_view_contract(self):
        """Проверяем удаление контракта"""
        self.client.login(username='test-manager', password='test123')

        contract = Contract.objects.create(
            name='Удаляемый',
            service=self.service,
            start_date='2024-01-01',
            end_date='2024-12-31',
            amount=1000
        )
        count_before = Contract.objects.count()

        response = self.client.post(reverse('contracts:delete', kwargs={'pk': contract.pk}))

        self.assertRedirects(response, reverse('contracts:list'))
        self.assertEqual(Contract.objects.count(), count_before - 1)
        self.assertFalse(Contract.objects.filter(pk=contract.pk).exists())
