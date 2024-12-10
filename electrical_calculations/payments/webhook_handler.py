from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import stripe
from django.conf import settings
from .models import Subscription, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        print(f"Signature verification failed: {e}")
        return HttpResponse(status=400)

    return handle_webhook_event(event)


# Processes specific Stripe webhook events and updates the database accordingly.
def handle_webhook_event(event):
    event_type = event['type']
    print(f"Received event: {event_type}")

    try:
        if event_type == 'invoice.payment_succeeded':
            handle_payment_succeeded(event['data']['object'])
        elif event_type == 'customer.subscription.deleted':
            handle_subscription_deleted(event['data']['object'])
        elif event_type == 'customer.subscription.updated':
            handle_subscription_updated(event['data']['object'])
        elif event_type == 'invoice.payment_failed':
            handle_payment_failed(event['data']['object'])
        else:
            print(f"Unhandled event type: {event_type}")
    except Exception as e:
        print(f"Error processing event: {e}")
        return HttpResponse(f"Error processing event: {str(e)}", status=500)

    return HttpResponse(status=200)


# Handles the invoice.payment_succeeded event.
def handle_payment_succeeded(invoice):
    subscription_id = invoice.get('subscription')
    payment_intent_id = invoice.get('payment_intent')
    amount_paid = invoice.get('amount_paid')  # Amount in cents
    currency = invoice.get('currency', 'usd')

    try:
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        Payment.objects.create(
            subscription=subscription,
            stripe_payment_intent_id=payment_intent_id,
            amount=amount_paid / 100,  # Convert cents to dollars
            currency=currency,
        )
        print(f"Payment succeeded for subscription: {subscription_id}")
    except Subscription.DoesNotExist:
        print(f"Subscription {subscription_id} not found for payment.")
        raise



# Handles the customer.subscription.deleted event.
def handle_subscription_deleted(subscription_data):
    subscription_id = subscription_data.get('id')
    try:
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        subscription.status = 'canceled'
        subscription.save()
        print(f"Subscription {subscription_id} canceled.")
    except Subscription.DoesNotExist:
        print(f"Subscription {subscription_id} not found.")
        raise



# Handles the customer.subscription.updated event.
def handle_subscription_updated(subscription_data):
    subscription_id = subscription_data.get('id')
    new_status = subscription_data.get('status')

    try:
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        subscription.status = new_status
        subscription.save()
        print(f"Subscription {subscription_id} updated to status: {new_status}")
    except Subscription.DoesNotExist:
        print(f"Subscription {subscription_id} not found.")
        raise



# Handles the invoice.payment_failed event.
def handle_payment_failed(invoice):
    subscription_id = invoice.get('subscription')
    try:
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
        subscription.status = 'past_due'
        subscription.save()
        print(f"Payment failed for subscription: {subscription_id}. Status updated to past_due.")
    except Subscription.DoesNotExist:
        print(f"Subscription {subscription_id} not found for failed payment.")
        raise


