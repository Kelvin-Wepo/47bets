from django.contrib import admin
from django.urls import path
from payment.views import pay_mpesa

urlpatterns = [
    path('', pay_mpesa )

]
 