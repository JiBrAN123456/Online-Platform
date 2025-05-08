from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.conf import settings

from .models import Payment, Transaction
from .serializers import TransactionSerializer
from .services import create_paypal_order
from courses.models import Course, Enrollment

import stripe
import requests

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateStripePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        amount = int(course.price * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            metadata={"course_id": course.id, "user_id": request.user.id}
        )

        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_payment_intent_id=intent["id"],
            amount=course.price,
            status="initiated"
        )

        return Response({"client_secret": intent["client_secret"]})


class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            payment_intent_id = intent['id']

            try:
                payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
                payment.status = 'succeeded'
                payment.save()
                Enrollment.objects.get_or_create(user=payment.user, course=payment.course)
            except Payment.DoesNotExist:
                return JsonResponse({'error': 'Payment not found'}, status=404)

        return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_paypal_payment(request):
    order = create_paypal_order(amount=20.00)  # Replace with course-based logic
    for link in order['links']:
        if link['rel'] == 'approve':
            return JsonResponse({'redirect_url': link['href']})
    return JsonResponse({'error': 'No approval URL found'}, status=400)


def get_paypal_access_token():
    res = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token',
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
        data={'grant_type': 'client_credentials'},
    )
    return res.json().get('access_token')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def capture_paypal_order(request):
    order_id = request.data.get('orderID')
    access_token = get_paypal_access_token()

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

    transaction = Transaction.objects.create(
        user=request.user,
        method='paypal',
        status='completed',
        amount=amount,
        currency=currency,
        transaction_id=transaction_id,
    )

    Payment.objects.create(
        transaction=transaction,
        payment_reference=order_id,
        paid_at=timezone.now(),
        user=request.user,
        status="succeeded"
    )

    return Response({'status': 'Payment successful'})


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
