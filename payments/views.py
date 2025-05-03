from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status


class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        payment =  serializer.save(user= self.request.user)
        payment.status = "initiated"
        payment.save()