from django.urls import path

from . import views

app_name = "lab3_shemelin"

urlpatterns = [
    path("clients/", views.client, name="clients"),
    path("offers/", views.offers, name='offers'),
    path("suppliers/", views.supplier, name='suppliers'),
    path("manufacturer/", views.manufacturer, name='manufacturer'),
    path("quipment/", views.quipment, name='quipment'),
    path("equipmentsales/", views.equipmentsales, name='equipmentsales'),
    path("staff/", views.staff, name='staff')
]