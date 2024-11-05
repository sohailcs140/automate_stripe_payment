from django.db import models


class Customer(models.Model):
    """Stripe Customer"""
    stripe_customer_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.stripe_customer_id)
