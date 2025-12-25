from django.shortcuts import render
from .models import Client, Offers, Suppliers, Manufacturer, Quipment, EquipmentSales, Staff

def client(request):
    clients = Client.objects.all()
    return render(request, 'lab3_shemelin/clients.html', {'clients':clients})
# Create your views here.


def offers(request):
    contracts = Offers.objects.all()
    return render(request, 'lab3_shemelin/offers.html', {'contracts':contracts})

def supplier(request):
    suppliers = Suppliers.objects.all()
    return render(request, 'lab3_shemelin/supplier.html', {'suppliers':suppliers})

def manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'lab3_shemelin/manufacturer.html', {'manufacturers':manufacturers})

def quipment(request):
    quipments = Quipment.objects.all()
    return render(request, 'lab3_shemelin/quipment.html', {'quipments':quipments})

def equipmentsales(request):
    equipmentsaless = EquipmentSales.objects.all()
    return render(request, 'lab3_shemelin/equipmentsales.html', {'equipmentsaless':equipmentsaless})

def staff(request):
    staffs = Staff.objects.all()
    return render(request, 'lab3_shemelin/staff.html', {'staffs':staffs})