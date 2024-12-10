from django.urls import path
from . import webhook_handler
from . import views


urlpatterns = [
    path('', views.subscription_page, name='payment_page'),
    path('create_subscription/', views.create_subscription, name='create_subscription'),
    path('cancel_subscription/', views.cancel_subscription, name='cancel_subscription'), 
    path('finalize_subscription/', views.finalize_subscription, name='finalize_subscription'),


    path('webhooks/', webhook_handler.stripe_webhook, name='stripe_webhook'),
]
