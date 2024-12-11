from payments.models import Subscription


def is_subscribe(request_user):
    try:
        subscription = Subscription.objects.filter(user=request_user, status__in=["active", "trialing", "incomplete"]).first()
        if subscription:
            has_subscription = subscription.status
        else:
            has_subscription = None

    except Subscription.DoesNotExist:
        has_subscription = None
    
    return has_subscription

