from django.urls import path
from . import views

urlpatterns = [

    # CATEGORY
    path("category/add/", views.vehicle_category, name="vehicle_category"),
    path("category/list/", views.vehicle_category_list, name="vehicle_category_list"),

    # VEHICLE
    path("vehicle/register/", views.register_vehicle, name="register_vehicle"),
    path("vehicle/list/", views.vehicle_registration_list, name="vehicle_registration_list"),

    # DASHBOARD
    path("dashboard/", views.dashboard, name="dashboard"),

    # CHECKOUT
    path("checkout/<int:pk>/", views.checkout_vehicle, name="checkout_vehicle"),
    path("receipt/print/<int:pk>/", views.print_receipt, name="print_receipt"),
]