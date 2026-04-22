from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # SERVICE PRICE (TYRE SETTINGS)
    # =========================
    path("price/add/", views.add_service_price, name="add_service_price"),
    path("price/list/", views.service_price_list, name="service_price_list"),

    # =========================
    # TYRE SECTION
    # =========================
    path("tyre/add/", views.add_tyre_service, name="add_tyre_service"),
    path("tyre/list/", views.tyre_list, name="tyre_list"),
    path("tyre/receipt/<int:pk>/", views.tyre_receipt, name="tyre_receipt"),

    # =========================
    # BATTERY SECTION
    # =========================
    path("battery/add/", views.add_battery_service, name="add_battery_service"),
    path("battery/list/", views.battery_list, name="battery_list"),
    path("battery/receipt/<int:pk>/", views.battery_receipt, name="battery_receipt"),
]