import enum

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class TransactionError(enum.Enum):
    ERROR = 0
    INVALID_ORIGIN_ACCOUNT = 1
    DOCUMENT_ID_DID_NOT_MATCH_ORIGIN_ACCOUNT = 2
    INSUFICIENT_FUNDS = 3
    INVALID_ORIGIN_CARD = 4
    CVC_DID_NOT_MATCH_ORIGIN_CARD = 5
    EXP_DATE_DID_NOT_MATCH_ORIGIN_CARD = 6
    EXP_DATE_EXPIRED_ORIGIN_CARD = 7
    INSUFICIENT_CREDITS = 8
    INVALID_TARGET_ACCOUNT = 9
    DOCUMENT_ID_DID_NOT_MATCH_TARGET_ACCOUNT = 10
    INVALID_TARGET_CARD = 11
    EXP_DATE_DID_NOT_MATCH_TARGET_CARD = 12
    EXP_DATE_EXPIRED_TARGET_CARD = 13
    TRANSACTION_TOOK_TOO_LONG = 14
    UNKNOWN_TRANSACTION_ERROR = 15

def get_error(code):
    if code == TransactionError.ERROR:
        raise serializers.ValidationError({"non_field_error": [_("Error with other bank")]})
    elif code == TransactionError.INVALID_ORIGIN_ACCOUNT or code == TransactionError.INVALID_ORIGIN_CARD:
        raise serializers.ValidationError(
            {"source": _("Invalid or non existent number")},
            code=code,
        )
    elif code == TransactionError.INSUFICIENT_FUNDS or code == TransactionError.INSUFICIENT_CREDITS:
        raise serializers.ValidationError(
            {"source": _("Does not have enough funds")},
            code=code,
        )
    elif code == TransactionError.CVC_DID_NOT_MATCH_ORIGIN_CARD:
        raise serializers.ValidationError(
            {"source": _("CVC did not match")},
            code=code,
        )
    elif code == TransactionError.EXP_DATE_EXPIRED_ORIGIN_CARD or code == TransactionError.EXP_DATE_DID_NOT_MATCH_ORIGIN_CARD:
        raise serializers.ValidationError(
            {"source": _("Date expired did not match or is expired")},
            code=code,
        )
    elif code == TransactionError.INVALID_TARGET_ACCOUNT or code == TransactionError.INVALID_TARGET_CARD:
        raise serializers.ValidationError(
            {"target": _("Invalid or non existent number")},
            code=code,
        )
    elif code == TransactionError.EXP_DATE_EXPIRED_TARGET_CARD or code == TransactionError.EXP_DATE_DID_NOT_MATCH_TARGET_CARD:
        raise serializers.ValidationError(
            {"target": _("Date expired did not match or is expired")},
            code=code,
        )
    elif code == TransactionError.DOCUMENT_ID_DID_NOT_MATCH_ORIGIN_ACCOUNT:
        raise serializers.ValidationError(
            {"original": _("Document id did not match")},
            code=code,
        )
    elif code == TransactionError.DOCUMENT_ID_DID_NOT_MATCH_TARGET_ACCOUNT:
        raise serializers.ValidationError(
            {"target": _("Document id did not match")},
            code=code,
        )
    else:
        raise serializers.ValidationError(
            {"non_field_error": [_("Error with other bank")]},
            code=code,
        )
