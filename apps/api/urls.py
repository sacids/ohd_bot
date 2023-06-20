from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('rumor-information', views.rumor_information, name='rumor-information'),
]