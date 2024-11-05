import stripe
from django.conf import settings
from django.shortcuts import redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import products

stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views import View
from .models import Customer


class StripeCheckOutView(View):
    """Checkout View"""

    def get(self, request):
        print(settings.DOMAIN)
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=products,
            mode='payment',
            customer_email="sohailcs@gmail.com",
            success_url=f"{settings.DOMAIN}" + 'payment-success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=f"{settings.DOMAIN}" + 'payment-cancel/',
        )

        return redirect(stripe_session.url)


def payment_success_view(request):
    print("*" * 10, "payment success", "*" * 10)

    session_id = request.GET.get('session_id')

    session = stripe.checkout.Session.retrieve(id=session_id)


    print(session.customer)

    return HttpResponse("payment success")


def payment_cancel_view(request):
    print("*" * 10, "payment cancel", "*" * 10)

    print(request.method)
    print(request.GET)
    return HttpResponse("payment cancel")

# acct_1QHOEIG01a9GyfhD
# web hook

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = "whsec_a941a5fe0da3786474d861f68618cb040433fed02f249187ad4a748c46686c39"  # Set this in your settings.py

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  # The session data
        customer_id = session.get('customer')
        print("*"*10, customer_id, "*"*10)
        print(f"Customer ID from webhook: {customer_id}")


    return HttpResponse({'status': 'success'}, status=200)