import gateway as gateway
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
        for subscription in gateway.get_subscriptions().items:
            self.update_user(subscription)

    def update_user(self, subscription):
        email = subscription.transactions[-1].customer['email']
        print("%s: status: %s; email: %s" %
              (subscription.id, subscription.status, email))
        user = self.models.User.query.filter_by(email=email).first()
        print("set: %s" % subscription.status == 'Active')
        if user:
            user.paid = subscription.status == 'Active'
        else:
            print("User with email not found: %s" % email)
        self.db.session.commit()

    def run(self):
        while not sleep(10):
            try:
                self.manage()
            except Exception as e:
                print(e)
