from django.contrib import admin
from django.urls import path
from payment.views import pay_mpesa

urlpatterns = [
      path('pay-mpesa/', pay_mpesa, name='pay_mpesa'),

]
 