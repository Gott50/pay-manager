import os
from dotenv import load_dotenv
import braintree

load_dotenv()

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)


def generate_client_token(customer_id=None):
    return gateway.client_token.generate({
        "customer_id": customer_id
    })


def subscription(userdata):
    customer = gateway.customer.create({
        "email": userdata.get("email")
    })

    payment_method = gateway.payment_method.create({
        "customer_id": customer.customer.id,
        "payment_method_nonce": userdata.get("nonce")
    })

    return create_subscription(payment_method, userdata)


def create_subscription(payment_method, userdata):
    if userdata.get("discount_code"):
        return gateway.subscription.create({
            "payment_method_token": payment_method.payment_method.token,
            "plan_id": "PinkParrotBasic",
            "discounts": {
                "add": [
                    {
                        "inherited_from_id": userdata.get("discount_code")
                    }
                ]
            }
        })
    else:
        return gateway.subscription.create({
            "payment_method_token": payment_method.payment_method.token,
            "plan_id": "PinkParrotBasic",
        })