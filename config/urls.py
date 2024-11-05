from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send/', views.msg_send_view, name="send"),
    path('receive/', views.msg_receive_view, name="re"),
    path('status/', views.msg_status_view, name="status"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("create-payment-intent/", views.CreatePaymentIntentView.as_view(), name="create-payment-intent"),
    path("create-auto-payment-intent/", views.CreateAutomaticPaymentIntentView.as_view(), name="create-auto-payment-intent"),

]
