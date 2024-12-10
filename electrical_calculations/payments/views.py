import stripe
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from .models import Subscription

import json


stripe.api_key = settings.STRIPE_SECRET_KEY



@login_required
def subscription_page(request):
    try:
        subscription = Subscription.objects.filter(user=request.user, status__in=["active", "trialing", "incomplete"]).first()
        if subscription:
            has_subscription = subscription.status 
        else:
            has_subscription = None

    except Subscription.DoesNotExist:
        has_subscription = None

    return render(request, 'payments/payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'has_subscription': has_subscription,
        'subscription_status': subscription.status if subscription else None,
    })



@login_required
def create_subscription(request):
    if request.method == "POST":
        try:
            existing_subscription = Subscription.objects.filter(user=request.user, status__in=["active", "trialing", "incomplete"]).first()
            
            if existing_subscription:
                return JsonResponse({'error': 'You already have an active or trialing subscription.'}, status=400)

            customer = None
            latest_subscription = Subscription.objects.filter(user=request.user).last()
            
            if not latest_subscription:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=request.user.get_full_name(),
                )
                stripe_customer_id = customer['id']
            else:
                stripe_customer_id = latest_subscription.stripe_customer_id

            subscription = stripe.Subscription.create(
                customer=stripe_customer_id,
                items=[{"price": settings.STRIPE_PRICE_ID}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
            )

            payment_intent = subscription['latest_invoice']['payment_intent']
            client_secret = payment_intent['client_secret']

            return JsonResponse({
                'subscriptionId': subscription['id'],
                'clientSecret': client_secret,
            })

        except IntegrityError:
            return JsonResponse({'error': 'Subscription creation failed due to a unique constraint issue.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@login_required
def finalize_subscription(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subscription_id = data.get('subscriptionId')
            payment_status = data.get('paymentStatus')

            if payment_status != 'succeeded':
                return JsonResponse({'error': 'Payment not completed successfully.'}, status=400)

            stripe_subscription = stripe.Subscription.retrieve(subscription_id)
            stripe_customer_id = stripe_subscription['customer']

            Subscription.objects.create(
                user=request.user,
                stripe_subscription_id=subscription_id,
                stripe_customer_id=stripe_customer_id,
                status=stripe_subscription['status'],
            )

            return JsonResponse({'message': 'Subscription finalized successfully.'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)




@login_required
def cancel_subscription(request):
    if request.method == "POST":
        try:
            subscription = Subscription.objects.get(user=request.user, status__in=["active", "trialing", "incomplete"])
            
            if subscription.status == 'canceled':
                return JsonResponse({'error': 'Subscription is already canceled.'}, status=400)
            
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=True,
            )

            subscription.status = 'canceled'
            subscription.save()

            return JsonResponse({'message': 'Subscription has been successfully canceled.'})

        except Subscription.DoesNotExist:
            return JsonResponse({'error': 'No active or trialing subscription found.'}, status=404)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Stripe error: {e.user_message}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


