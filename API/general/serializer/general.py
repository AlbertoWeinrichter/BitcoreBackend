from rest_framework import serializers

from API.general.models.general import ContactForm
from API.user.models.user import TagFollow, User

from ..models.general import Ad, CustomTag, Quote


class ContactFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'


class PublicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTag
        fields = '__all__'

    def to_representation(self, instance):
        data = super(TagSerializer, self).to_representation(instance)

        try:
            user = User.objects.get(username=self.context["request"].user)
            already_following = TagFollow.objects.filter(tag=instance,
                                                         follower=user.id)
            if len(already_following) > 0:
                data.update({"already_following": True})
        except User.DoesNotExist:
            data.update({"already_following": False})

        return data
