from rest_framework import serializers
from .models import Payment ,Transaction



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['status', 'created_at', 'updated_at', 'transaction_id', 'user']



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'course', 'amount', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at', 'user']



        def create(self,validated_data):
            request = self.context["request"]
            validated_data['user'] = request.user
            return super().create(validated_data)