import os
from dotenv import load_dotenv

import stripe

load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

PLAN_ID = "PinkParrotBasic"


def subscription(userdata, print=print):
    customer = stripe.Customer.create(
        email=userdata.get('email'),
        source=userdata.get('token')  # obtained with Stripe.js
    )

    return stripe.Subscription.create(
        customer=customer.id,
        items=[
            {
                "plan": "PinkParrotBeta",
            },
        ],
        coupon=userdata.get('discount_code')
    )


def get_subscriptions():
    return {"items": []}