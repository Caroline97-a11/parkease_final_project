from django.urls import path
from .import views
urlpatterns =[
    path('', views.loginPage, name = 'loginPage'),
    path('staff/', views.register, name='register')

]