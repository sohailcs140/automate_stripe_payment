import json
import urllib.parse

import stripe
from django.conf import settings
from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def msg_receive_view(reqeust):
    if reqeust.method == "POST":
        print("*" * 20, "message receive", "*" * 20)

        parsed_data = urllib.parse.parse_qs(reqeust.body.decode('utf-8'))

        for key, value in parsed_data.items():
            print(key, value)

        return HttpResponse("message receive")

    return HttpResponse("METHOD NOT ALLOWED")


def msg_send_view(request):
    account_sid = 'ACccce024270f43a7f17534c59abb6ff4c'
    auth_token = 'd1ead85e75f45c2bac33f75644fa3ac6'
    client = Client(account_sid, auth_token)

    print("*" * 20, "message send", "*" * 20)

    content_variables = json.dumps({"1": request.POST.get('name'), "2": request.POST.get('message')}
                                   )
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        content_sid='HX36dc82bec8137e2d7e31f358fae270a5',
        content_variables=content_variables,
        to='whatsapp:+923150575122'
    )

    return HttpResponse(f"message send {message.sid}")


@csrf_exempt
def msg_status_view(request):
    print("*" * 20, "status of view", "*" * 20)

    data = urllib.parse.parse_qs(qs=request.body.decode("utf-8"))

    for key, value in data.items():
        print(key, value)

    return HttpResponse("message status change")


# Stripe

@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentIntentView(View):
    def get(self, request):

        return render(request, "stripe.html")

    def post(self, request):
        # Ensure the Stripe secret key is set
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the payment amount and currency from the request
        amount = 16 * 100  # Example amount in cents ($20.00)
        currency = 'usd'  # Use your desired currency

        # You would get these details from your frontend (e.g., after the user entered card details)
        data = json.loads(request.body)

        payment_method_id = data.get('payment_method_id')
        customer_email = data.get('customer_email')

        try:
            # Create the customer (you only need to do this once)
            customer = stripe.Customer.create(
                email=customer_email,  # Optional, but useful for identifying the user
            )

            # Save the payment method to the customer
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer.id,
            )

            # Set the customer’s default payment method
            stripe.Customer.modify(
                customer.id,
                invoice_settings={'default_payment_method': payment_method_id}
            )

            # Create a PaymentIntent to charge the customer
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                customer=customer.id,
                payment_method=payment_method.id,
                # off_session=True,  # This means you are processing the payment off-session
                # confirm=True,  # Confirm the payment immediately
            )

            print("*" * 10, payment_intent, "*" * 10)
            # Return the client secret to the frontend
            return HttpResponse(json.dumps({
                'client_secret': payment_intent.client_secret,
                'customer_id': payment_intent.customer
            }))

        except stripe.error.StripeError as e:
            # Handle errors
            return HttpResponse(json.dumps({'error': str(e)}))


@method_decorator(csrf_exempt, name='dispatch')
class CreateAutomaticPaymentIntentView(View):
    def post(self, request):
        # Ensure the Stripe secret key is set
        stripe.api_key = settings.STRIPE_SECRET_KEY

        amount = 2000
        customer_id = json.loads(request.body).get('customer_id')
        currency = 'usd'
        try:
            customer = stripe.Customer.retrieve(customer_id)
            default_payment_method = customer.invoice_settings.default_payment_method

            if not default_payment_method:
                return HttpResponse(json.dumps({'error': 'No default payment method found'}))

            # Create the PaymentIntent for the subsequent charge
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                customer=customer_id,
                payment_method=default_payment_method,
                off_session=True,  # Off-session payment (without user intervention)
                confirm=True,  # Confirm the payment immediately
            )

            # Return the client secret (you can return this to the frontend if needed)
            return HttpResponse(json.dumps({
                'client_secret': payment_intent.client_secret
            }))

        except stripe.error.StripeError as e:
            return HttpResponse(json.dumps({'error': str(e)}))
