from django.urls import path

import app.payment_views as payment_views

urlpatterns = [
    path('checkout/', payment_views.StripeCheckOutView.as_view(), name="checkout"),
    path('payment-success/', payment_views.payment_success_view, name="payment-success"),
    path('payment-cancel/', payment_views.payment_cancel_view, name="payment-cancel"),
    path('webhook/', payment_views.webhook, name="webhook"),
]
