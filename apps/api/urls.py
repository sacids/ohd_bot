from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('pull', views.pull, name='pull'),
    path('loans', views.loans, name='loans'),
    path('repayments', views.repayments, name='repayments'),
    path('insurance-information', views.insurance_information, name='insurance-information'),
]