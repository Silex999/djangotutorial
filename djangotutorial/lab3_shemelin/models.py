from django.db import models

class Client(models.Model):
    client_id = models.AutoField(primary_key=True) 
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, null=True)
    passport = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True)
    phone = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.client_id)

class Offers(models.Model):
    contract_id = models.AutoField(primary_key=True)
    contract_number = models.IntegerField()
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    signing_date = models.DateField()
    signing_place = models.CharField(max_length=100)
    expiration_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)

class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=100)
    price = models.IntegerField()

class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    mail = models.CharField(max_length=100)
    price = models.IntegerField()

class Quipment(models.Model):
    id = models.AutoField(primary_key=True)
    manufacturer = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.IntegerField()

class EquipmentSales(models.Model):
    id = models.AutoField(primary_key=True)
    clients = models.CharField(max_length=100)
    staff = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    price = models.IntegerField()

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
