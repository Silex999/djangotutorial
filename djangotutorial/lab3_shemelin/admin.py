from django.contrib import admin

from .models import Client
from .models import Offers
from .models import Suppliers
from .models import Manufacturer
from .models import Quipment
from .models import EquipmentSales
from .models import Staff

admin.site.register(Client)
admin.site.register(Offers)
admin.site.register(Suppliers)
admin.site.register(Manufacturer)
admin.site.register(Quipment)
admin.site.register(EquipmentSales)
admin.site.register(Staff)

# Register your models here.
