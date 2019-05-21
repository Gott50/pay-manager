import os
from dotenv import load_dotenv

import stripe

load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

PLAN_ID = "PINKPARROT_MONTHLY"


def subscription(userdata, print=print):
    customer = stripe.Customer.create(
        email=userdata.get('email'),
        source=userdata.get('token')  # obtained with Stripe.js
    )

    if userdata.get('discount_code') and len(userdata.get('discount_code')) > 0:
        return stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": "PinkParrotBeta",
                },
            ],
            coupon=userdata.get('discount_code')
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


def get_subscriptions():
    return {"items": []}