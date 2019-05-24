import os
from dotenv import load_dotenv

import stripe

load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

PLAN_ID = "PINKPARROT_MONTHLY"


def subscription(customer, discount_code, print=print):
    if discount_code and len(discount_code) > 0:
        return stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": "PinkParrotBeta",
                },
            ],
            coupon=discount_code
        )
    else:
        return stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": "PinkParrotBeta",
                },
            ]
        )


def get_customer(email, source, print=print):
    try:
        customers = stripe.Customer.list(email=email, limit=1)
        customer = customers['data'][0]
    except Exception as e:
        print(e)
        customer = stripe.Customer.create(
            email=email,
            source=source
        )
    print("get_customer() created customer: %s" % customer)
    return customer


def get_coupon(discount_code, print=print):
    retrieve = stripe.Coupon.retrieve(discount_code)
    return retrieve


def modify_costomer(email, source, print=print):
    customer = get_customer(email=email, source=source)

    try:
        retrieve = stripe.Customer.modify(
            customer.id,
            source=source
        )
    except Exception as e:
        print(e)
        retrieve = subscription(customer=customer, print=print)

    return retrieve


def get_subscriptions():
    return {"items": []}