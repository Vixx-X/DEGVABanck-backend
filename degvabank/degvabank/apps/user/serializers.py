from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.urls.base import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import _unicode_ci_compare
from django.contrib.sites.shortcuts import get_current_site
from django_otp import verify_token

from .models import User
from degvabank.apps.account.models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "document_id",
            "type",
            "first_name",
            "last_name",
        ]

def get_password_reset_url(user, token_generator=default_token_generator):
    """
    Generate a password-reset URL for a given user
    """
    kwargs = {
        "token": token_generator.make_token(user),
        "uidb64": urlsafe_base64_encode(force_bytes(user.id)),
    }
    return reverse("password-reset-confirm", kwargs=kwargs)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        site = get_current_site(request)
        if domain_override is not None:
            site.domain = site.name = domain_override
        for user in self.get_users(self.data["email"]):
            self.send_password_reset_email(site, user)

    def send_password_reset_email(self, site, user):
        extra_context = {
            "user": user,
            "site": site,
            "reset_url": get_password_reset_url(user),
        }
        # CustomerDispatcher().send_password_reset_email_for_user(user, extra_context)


class PasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.user = self.context['request'].user

    def validate(self, attrs):
        password1 = attrs["new_password1"]
        password2 = attrs["new_password2"]
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    _("The two password fields didn’t match."),
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self):
        password = self.validated_data
        self.user.set_password(password)
        self.user.save()
        return self.user


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    device = serializers.CharField(read_only=True)


class OTPChallengeSerializer(serializers.Serializer):
    device = serializers.CharField()
    token = serializers.CharField()

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.user = self.context['request'].user


    def validate_token(self, token):
        data = self.get_initial()
        device = data['device']
        verified = verify_token(user=self.user, device_id=device, token=token) is not None
        if not verified:
            raise ValidationError(
                _("The token submitted is invalid."),
                code="token_invalid",
            )

class ChangePasswordSerializer(OTPChallengeSerializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate_old_password(self, old_password):
        if not self.user.check_password(old_password):
            raise ValidationError(
                _("The old password didn’t match."),
                code="wrong_password",
            )

    def validate(self, attrs):
        super().validate(attrs)

        password1 = attrs["new_password1"]
        password2 = attrs["new_password2"]
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    _("The two password fields didn’t match."),
                    code="password_mismatch",
                )

        password_validation.validate_password(password2, self.user)
        return password2

    def save(self):
        password = self.validated_data
        self.user.set_password(password)
        self.user.save()
        return self.user


class ChangeEmailSerializer(OTPChallengeSerializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if email == self.user.email:
            raise ValidationError(
                _("The email has not changed."),
                code="repeated_email",
            )

        if User.objects.filter(email=email).count():
            raise ValidationError(
                _("The email is already in use."),
                code="used_email",
            )

    def validate(self, attrs):
        super().validate(attrs)
        return attrs["email"]

    def save(self):
        email = self.validated_data
        self.user.email = email
        self.user.save()
        return self.user

class RegisterUserSerializer(UserProfileSerializer):
    password1 = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )
    account_type = serializers.ChoiceField(choices=Account.AccountType.choices)

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("A user with this email allready exists")

        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match")

        try:
            password_validation.validate_password(attrs["password1"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs


    def save(self):
        email = self.validated_data["email"]
        password = self.validated_data["password1"]
        user = User.objects.create_user(username=email, email=email, password=password)
        Account(type=self.validated_data["account_type"]).save()

        return user

    class Meta(UserProfileSerializer.Meta):
        fields = UserProfileSerializer.Meta.fields + [
            "password1",
            "password2",
            "account_type",
        ]
