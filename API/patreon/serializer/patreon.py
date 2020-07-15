from rest_framework import serializers

from API.patreon.models.patreon import PatreonImage, Survey


class PatreonSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        exclude = ("id",)


class PatreonImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatreonImage
        fields = "__all__"
