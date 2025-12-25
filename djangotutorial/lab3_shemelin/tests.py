from django.test import TestCase, Client as TestClient
from django.urls import reverse
from datetime import date, timedelta
from decimal import Decimal

from .models import (
    Client, Offers, Suppliers, Manufacturer, 
    Quipment, EquipmentSales, Staff
)


# тесты моделей

class ClientModelTest(TestCase):
    
    def setUp(self):
        self.client_data = {
            'surname': 'Иванов',
            'name': 'Иван',
            'patronymic': 'Иванович',
            'passport': '1234 567890',
            'address': 'г. Москва, ул. Ленина, 1',
            'email': 'ivanov@example.com',
            'phone': '+7-999-123-45-67'
        }
    
    def test_client_creation(self):
        client = Client.objects.create(**self.client_data)
        self.assertEqual(client.surname, 'Иванов')
        self.assertEqual(client.name, 'Иван')
        self.assertEqual(client.email, 'ivanov@example.com')
        self.assertIsNotNone(client.client_id)
    
    def test_client_str_method(self):
        client = Client.objects.create(**self.client_data)
        self.assertEqual(str(client), str(client.client_id))
    
    def test_client_without_optional_fields(self):
        client = Client.objects.create(
            surname='Петров',
            name='Петр',
            passport='9876 543210',
            phone='+7-888-999-00-11'
        )
        self.assertIsNone(client.patronymic)
        self.assertIsNone(client.address)
        self.assertIsNone(client.email)
    
    def test_email_validation(self):
        client = Client.objects.create(
            surname='Сидоров',
            name='Сидор',
            passport='1111 222222',
            phone='+7-777-777-77-77',
            email='valid@email.com'
        )
        self.assertTrue('@' in client.email)


class OffersModelTest(TestCase):
    
    def setUp(self):
        self.client = Client.objects.create(
            surname='Тестов',
            name='Тест',
            passport='0000 000000',
            phone='+7-000-000-00-00'
        )
    
    def test_offer_creation(self):
        offer = Offers.objects.create(
            contract_number=12345,
            client_id=self.client,
            signing_date=date.today(),
            signing_place='г. Москва',
            expiration_date=date.today() + timedelta(days=365),
            total_amount=Decimal('50000.00')
        )
        self.assertEqual(offer.contract_number, 12345)
        self.assertEqual(offer.client_id, self.client)
        self.assertEqual(offer.total_amount, Decimal('50000.00'))
    
    def test_offer_cascade_delete(self):
        offer = Offers.objects.create(
            contract_number=999,
            client_id=self.client,
            signing_date=date.today(),
            signing_place='г. СПб',
            expiration_date=date.today() + timedelta(days=180)
        )
        client_id = self.client.client_id
        self.client.delete()
        
        self.assertFalse(Offers.objects.filter(contract_id=offer.contract_id).exists())
    
    def test_offer_without_total_amount(self):
        offer = Offers.objects.create(
            contract_number=777,
            client_id=self.client,
            signing_date=date.today(),
            signing_place='г. Казань',
            expiration_date=date.today() + timedelta(days=90)
        )
        self.assertIsNone(offer.total_amount)


class SuppliersModelTest(TestCase):
    
    def test_supplier_creation(self):
        supplier = Suppliers.objects.create(
            title='ООО "Техника"',
            phone_number=79991234567,
            address='г. Москва, ул. Поставщиков, 10',
            price=100000
        )
        self.assertEqual(supplier.title, 'ООО "Техника"')
        self.assertEqual(supplier.price, 100000)
        self.assertIsNotNone(supplier.id)


class ManufacturerModelTest(TestCase):
    
    def test_manufacturer_creation(self):
        manufacturer = Manufacturer.objects.create(
            title='Samsung Electronics',
            phone_number=74951234567,
            mail='info@samsung.com',
            price=250000
        )
        self.assertEqual(manufacturer.title, 'Samsung Electronics')
        self.assertEqual(manufacturer.mail, 'info@samsung.com')


class QuipmentModelTest(TestCase):
    
    def test_equipment_creation(self):
        equipment = Quipment.objects.create(
            manufacturer='Apple',
            color='Черный',
            quantity=50,
            price=75000
        )
        self.assertEqual(equipment.manufacturer, 'Apple')
        self.assertEqual(equipment.quantity, 50)
        self.assertEqual(equipment.color, 'Черный')
    
    def test_equipment_quantity_update(self):
        equipment = Quipment.objects.create(
            manufacturer='Xiaomi',
            color='Белый',
            quantity=100,
            price=25000
        )
        equipment.quantity = 80
        equipment.save()
        
        updated_equipment = Quipment.objects.get(id=equipment.id)
        self.assertEqual(updated_equipment.quantity, 80)


class EquipmentSalesModelTest(TestCase):
    
    def test_sale_creation(self):
        sale = EquipmentSales.objects.create(
            clients='Иванов И.И.',
            staff='Петров П.П.',
            date=date.today(),
            quantity=5,
            price=15000
        )
        self.assertEqual(sale.clients, 'Иванов И.И.')
        self.assertEqual(sale.quantity, 5)
        self.assertEqual(sale.date, date.today())


class StaffModelTest(TestCase):
    
    def test_staff_creation(self):
        staff = Staff.objects.create(
            lastname='Работников',
            patronymic='Работникович',
            address='г. Екатеринбург, пр. Ленина, 50',
            post='Менеджер'
        )
        self.assertEqual(staff.lastname, 'Работников')
        self.assertEqual(staff.post, 'Менеджер')


# тесты представлений (views)

class ClientViewTest(TestCase):
    
    def test_clients_view_without_data(self):
        response = self.client.get(reverse('lab3_shemelin:clients'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Данные отсутствуют')
        self.assertQuerySetEqual(response.context['clients'], [])
    
    def test_clients_view_with_data(self):
        client1 = Client.objects.create(
            surname='Иванов',
            name='Иван',
            passport='1234 567890',
            phone='+7-999-111-11-11'
        )
        client2 = Client.objects.create(
            surname='Петров',
            name='Петр',
            passport='9876 543210',
            phone='+7-999-222-22-22'
        )
        
        response = self.client.get(reverse('lab3_shemelin:clients'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иванов')
        self.assertContains(response, 'Петров')
        self.assertEqual(len(response.context['clients']), 2)
    
    def test_clients_view_template_used(self):
        response = self.client.get(reverse('lab3_shemelin:clients'))
        self.assertTemplateUsed(response, 'lab3_shemelin/clients.html')


class OffersViewTest(TestCase):
    
    def setUp(self):
        self.client_obj = Client.objects.create(
            surname='Тестов',
            name='Тест',
            passport='0000 000000',
            phone='+7-000-000-00-00'
        )
    
    def test_offers_view_without_data(self):
        response = self.client.get(reverse('lab3_shemelin:offers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Данные отсутствуют')
    
    def test_offers_view_with_data(self):
        offer = Offers.objects.create(
            contract_number=12345,
            client_id=self.client_obj,
            signing_date=date.today(),
            signing_place='г. Москва',
            expiration_date=date.today() + timedelta(days=365)
        )
        
        response = self.client.get(reverse('lab3_shemelin:offers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '12345')
        self.assertContains(response, 'г. Москва')


class SuppliersViewTest(TestCase):
    
    def test_suppliers_view_without_data(self):
        response = self.client.get(reverse('lab3_shemelin:suppliers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Данные отсутствуют')
    
    def test_suppliers_view_with_data(self):
        supplier = Suppliers.objects.create(
            title='ООО "Техника"',
            phone_number=79991234567,
            address='г. Москва',
            price=100000
        )
        
        response = self.client.get(reverse('lab3_shemelin:suppliers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ООО "Техника"')


class ManufacturerViewTest(TestCase):
    
    def test_manufacturer_view_status_code(self):
        response = self.client.get(reverse('lab3_shemelin:manufacturer'))
        self.assertEqual(response.status_code, 200)
    
    def test_manufacturer_view_with_data(self):
        manufacturer = Manufacturer.objects.create(
            title='Samsung',
            phone_number=74951234567,
            mail='info@samsung.com',
            price=250000
        )
        
        response = self.client.get(reverse('lab3_shemelin:manufacturer'))
        self.assertContains(response, 'Samsung')


class QuipmentViewTest(TestCase):
    
    def test_quipment_view_with_data(self):
        equipment = Quipment.objects.create(
            manufacturer='Apple',
            color='Черный',
            quantity=50,
            price=75000
        )
        
        response = self.client.get(reverse('lab3_shemelin:quipment'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Черный')


class EquipmentSalesViewTest(TestCase):
    
    def test_equipmentsales_view_status_code(self):
        response = self.client.get(reverse('lab3_shemelin:equipmentsales'))
        self.assertEqual(response.status_code, 200)
    
    def test_equipmentsales_view_with_data(self):
        sale = EquipmentSales.objects.create(
            clients='Иванов И.И.',
            staff='Петров П.П.',
            date=date.today(),
            quantity=5,
            price=15000
        )
        
        response = self.client.get(reverse('lab3_shemelin:equipmentsales'))
        self.assertContains(response, 'Иванов И.И.')


class StaffViewTest(TestCase):
    
    def test_staff_view_with_data(self):
        staff = Staff.objects.create(
            lastname='Работников',
            patronymic='Работникович',
            address='г. Екатеринбург',
            post='Менеджер'
        )
        
        response = self.client.get(reverse('lab3_shemelin:staff'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Работников')
        self.assertContains(response, 'Менеджер')


# интеграционные тесты

class IntegrationTests(TestCase):
    
    def test_client_with_multiple_offers(self):
        client = Client.objects.create(
            surname='Многоконтрактный',
            name='Клиент',
            passport='1111 111111',
            phone='+7-111-111-11-11'
        )
        
        offer1 = Offers.objects.create(
            contract_number=1,
            client_id=client,
            signing_date=date.today(),
            signing_place='Москва',
            expiration_date=date.today() + timedelta(days=365)
        )
        
        offer2 = Offers.objects.create(
            contract_number=2,
            client_id=client,
            signing_date=date.today(),
            signing_place='СПб',
            expiration_date=date.today() + timedelta(days=180)
        )
        
        self.assertEqual(client.offers_set.count(), 2)
    
    def test_all_views_accessible(self):
        urls = [
            'clients', 'offers', 'suppliers', 'manufacturer',
            'quipment', 'equipmentsales', 'staff'
        ]
        
        for url_name in urls:
            response = self.client.get(reverse(f'lab3_shemelin:{url_name}'))
            self.assertEqual(
                response.status_code, 200,
                f'Страница {url_name} недоступна'
            )