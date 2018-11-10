import src.gateway as gateway
from time import sleep


class Manager:
    def __init__(self, db, models):
        """

        :type db: flask_sqlalchemy.SQLAlchemy
        :type models: models
        """
        self.db = db
        self.models = models

    def manage(self):
        result = gateway.get_subscriptions()
        print(result)
        for subscription in result.items:
            print("%s: status: %s; email: %s" %
                  (subscription.id, subscription.status, subscription.transactions[-1].customer['email']))

    def run(self):
        while not sleep(10):
            try:
                self.manage()
            except Exception as e:
                print(e)
