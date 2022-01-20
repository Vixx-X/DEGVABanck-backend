from simple_mail.mailer import BaseSimpleMail, simple_mailer
from .models import User

class EMAIL_TYPES:
    WELCOME = "welcome"
    SEND_OTP = "send_otp"


class BaseSimpleMail(BaseSimpleMail):

    def set_context(self, ctx={}):
        self.context = { **self.context, **ctx}


class WelcomeMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.WELCOME
    context = {
        "welcome_link": "https://google.com"
    }

    def set_context(self, user, welcome_link=None):
        ctx = { "user":user }
        if (welcome_link):
            ctx["welcome_link"] = welcome_link
        super().set_context(ctx=ctx)


class SendOTPMail(BaseSimpleMail):
    email_key = EMAIL_TYPES.SEND_OTP
    context = {
        "user": "admin",
        "token": 123456,
    }

    def set_context(self, user, token):
        ctx = { "user":user, "token":token }
        super().set_context(ctx=ctx)


simple_mailer.register(WelcomeMail)
simple_mailer.register(SendOTPMail)
