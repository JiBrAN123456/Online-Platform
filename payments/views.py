from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer , TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Payment ,Transaction
from courses.models import Course
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from courses.models import Enrollment
from rest_framework import viewsets, permissions
from .services import create_paypal_order
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
import requests

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
    


class TransactionViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()     
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)
    

    def perform_create(self, serializer):
        serializer.save(user= self.request.user, status= "completed")




def create_payment_view(request):

    order = create_paypal_order(amount=20.00)
    for link in order['links']:
        if link['rel'] == 'approve':
            return JsonResponse({'redirect_url': link['href']})
    return JsonResponse({"error": "No approval URL found"}, status=400)    


def get_paypal_access_token():
    res = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token',
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
        data={'grant_type': 'client_credentials'},
    )
    return res.json().get('access_token')

# 2. Capture Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def capture_order(request):
    order_id = request.data.get('orderID')
    access_token = get_paypal_access_token()

    # Capture the order
    response = requests.post(
        f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        },
    )

    data = response.json()
    if response.status_code != 201:
        return Response({'error': 'Capture failed', 'details': data}, status=400)

    transaction_id = data['purchase_units'][0]['payments']['captures'][0]['id']
    amount = data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
    currency = data['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']

    # Save transaction
    transaction = Transaction.objects.create(
        user=request.user,
        method='paypal',
        status='completed',
        amount=amount,
        currency=currency,
        transaction_id=transaction_id,
    )

    # Save payment
    Payment.objects.create(
        transaction=transaction,
        payment_reference=order_id,
        paid_at=timezone.now(),
    )

    return Response({'status': 'Payment successful'})