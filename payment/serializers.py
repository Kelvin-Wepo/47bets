from payment.models import Transaction
from rest_framework import serializers 

class TransactionSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = '__all__'

