from simple_mail.mailer import BaseSimpleMail, simple_mailer

from degvabank.apps.transaction.models import Transaction


class EMAIL_TYPES:
    WELCOME = "welcome"
    SEND_OTP = "send_otp"
    TRANS_RECEIVE = "transaction receive"
    TRANS_SENT = "transaction sent"
    RESET_PASS = "reset password"
    CHANGE_USER = "change user"


class BaseSimpleMail(BaseSimpleMail):
    def set_context(self, ctx={}):
        self.context = {**self.context, **ctx}


class WelcomeMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.WELCOME
    context = {"welcome_link": "https://google.com"}

    def set_context(self, user, welcome_link=None):
        ctx = {"user": user}
        if welcome_link:
            ctx["welcome_link"] = welcome_link
        super().set_context(ctx=ctx)


class SendOTPMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.SEND_OTP
    context = {
        "user": "admin",
        "token": 123456,
    }

    def set_context(self, user, token):
        ctx = {"user": user, "token": token}
        super().set_context(ctx=ctx)


class TransactionReceiveMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.TRANS_RECEIVE
    context = {"user": "admin", "transaction": Transaction.get_dommy()}

    def set_context(self, user, transaction):
        ctx = {"user": user, "transaction": transaction}
        return super().set_context(ctx)

    def set_test_context(self):
        from .models import User
        user = User.objects.first()
        transaction = Transaction.get_dommy()
        self.set_context(user, transaction)


class TransactionSentMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.TRANS_SENT
    context = {"user": "admin", "transaction": Transaction.get_dommy()}

    def set_context(self, user, transaction):
        ctx = {"user": user, "transaction": transaction}
        return super().set_context(ctx)

    def set_test_context(self):
        from .models import User
        user = User.objects.first()
        transaction = Transaction.get_dommy()
        self.set_context(user, transaction)


class ResetPasswordMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.RESET_PASS
    context = {"user": "admin", "url": "https://bank.vittorioadesso.com/"}

    def set_context(self, user, url):
        ctx = {"user": user, "url": url}
        return super().set_context(ctx)

    def set_test_context(self):
        from .models import User
        user = User.objects.first()
        url = "https://bank.vittorioadesso.com/"
        self.set_context(user, url)


class ResetUserMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.CHANGE_USER
    context = {"user": "admin"}

    def set_context(self, user):
        ctx = {"user": user}
        return super().set_context(ctx)

    def set_test_context(self):
        from .models import User
        user = User.objects.first()
        self.set_context(user)


simple_mailer.register(WelcomeMail)
simple_mailer.register(SendOTPMail)
simple_mailer.register(TransactionReceiveMail)
simple_mailer.register(TransactionSentMail)
simple_mailer.register(ResetPasswordMail)
simple_mailer.register(ResetUserMail)
