import src.gateway as gateway
from time import sleep


def manage():
    result = gateway.get_subscriptions()
    print(result)
    for subscription in result.items:
        print("%s: status: %s" %
              (subscription.id, subscription.status))


if __name__ == '__main__':
    while not sleep(10):
        manage()
