from rest_framework import serializers
from .models import Payment



class PaymentSerializewr(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['status', 'created_at', 'updated_at', 'transaction_id', 'user']

