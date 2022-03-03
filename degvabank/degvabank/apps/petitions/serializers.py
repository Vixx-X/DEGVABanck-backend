from rest_framework import serializers

from .models import Petition


class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = "__all__"


class UserPetitionSerializer(serializers.ModelSerializer):

    reason = serializers.CharField(source="get_reason_display")

    class Meta:
        model = Petition
        exclude = ["user", "content_type"]
