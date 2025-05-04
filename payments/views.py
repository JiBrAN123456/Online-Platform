from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Payment
from courses.models import Course




class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        payment =  serializer.save(user= self.request.user)
        payment.status = "initiated"
        payment.save()




stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        course_id  = self.request.get("course_id")
        try:
            course = Course.objects.get(id= course_id)
        except Course.DoesNotExist:
            return Response({"error":"Course not found"}, status=status.HTTP_404_NOT_FOUND) 

        amount = int(course.price * 100)

        intent = stripe.PaymentIntent.create(
            user = request.user,
            course=course,
            stripe_payment_intent_id = intent["id"],
            amount = course_id
        )



        Payment.objects.create (
            user = request.user,
            course = course,
            stripe_payment_intent_id = intent["id"],
            amount = course.price

        )           


        return Response({"client_secret": intent["client_secret"]})
    