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
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from courses.models import Enrollment



class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        payment =  serializer.save(user= self.request.user)
        payment.status = "initiated"
        payment.save()




stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET 


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
    



class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        paylaod = request.body
        sig_header = request.META.get("HTTP_STRIDE_SIGNATURE")


        try:
            event = stripe.Webhook.construct_event(
                paylaod, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status= 400)

        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            payment_intent_id = intent['id']

            try:
                payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
                payment.status = 'succeeded'
                payment.save()

                # Grant access (e.g., enroll user in course) – we can do that next
            except Payment.DoesNotExist:
                return JsonResponse({'error': 'Payment not found'}, status=404)
            


            try:
                payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
                payment.status = "succeeded"
                payment.save()

                Enrollment.objects.get_or_create(
                    user= payment.user,
                    course= payment.course

                )
            except Payment.DoesNotExist:
                return JsonResponse({"error":"Payment not found"}, status= 404)    

        return HttpResponse(status=200)    