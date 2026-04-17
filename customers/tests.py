from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from services.models import Service
from users.models import User


class CustomerListViewTestCase(TestCase):
    """Тесты для проверки CRUD Активных клиентов и прав доступа."""
    fixtures = ['roles.json']

    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create_user(username='test-manager', password='test123')
        cls.marketer = User.objects.create_user(username='test-marketer', password='test123')

        cls.manager.groups.add(Group.objects.get(name='Менеджеры'))
        cls.marketer.groups.add(Group.objects.get(name='Маркетологи'))

        cls.service = Service.objects.create(name='Услуга', description='...', price=1000)
        cls.contract = Contract.objects.create(
            name='Контракт',
            service=cls.service,
            start_date='2024-01-01',
            end_date='2024-12-31',
            amount=50000
        )
        cls.lead = Lead.objects.create(
            first_name='Иван',
            last_name='Петров',
            middle_name='Сергеевич',
            telephone='84955555555',
            email='ivan@some.ru'
        )

        cls.customer = Customer.objects.create(
            lead=cls.lead,
            contract=cls.contract
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('customers:list'))
        self.assertRedirects(response, '/login/?next=/customers/')

    def test_access_for_manager(self):
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)

    def test_forbidden_for_marketer(self):
        self.client.login(username='test-marketer', password='test123')
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 403)

    def test_list_view_displays_customer(self):
        self.client.login(username='test-manager', password='test123')
        response = self.client.get(reverse('customers:list'))
        self.assertContains(response, 'Петров Иван')

    def test_create_customer_from_lead(self):
        """Активация лида, создание клиента"""
        self.client.login(username='test-manager', password='test123')

        new_lead = Lead.objects.create(
            first_name='Петр',
            last_name='Сидоров',
            telephone='84959999999',
            email='petr@mail.ru'
        )
        count_before = Customer.objects.count()

        response = self.client.post(
            reverse('customers:create_from_lead', kwargs={'lead_pk': new_lead.pk}),
            {'contract': self.contract.pk}
        )

        self.assertRedirects(response, reverse('customers:list'))
        self.assertEqual(Customer.objects.count(), count_before + 1)
        self.assertTrue(Customer.objects.filter(lead=new_lead).exists())

    def test_delete_customer(self):
        self.client.login(username='test-manager', password='test123')

        customer = Customer.objects.create(
            lead=Lead.objects.create(first_name='Удаляемый', last_name='Клиент', telephone='123', email='a@b.ru'),
            contract=self.contract
        )
        count_before = Customer.objects.count()

        response = self.client.post(reverse('customers:delete', kwargs={'pk': customer.pk}))

        self.assertRedirects(response, reverse('customers:list'))
        self.assertEqual(Customer.objects.count(), count_before - 1)
