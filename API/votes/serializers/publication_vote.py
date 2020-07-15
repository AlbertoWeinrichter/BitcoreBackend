from rest_framework import serializers

from API.votes.models.post_vote import PublicationVote


class PublicationVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationVote
        fields = '__all__'


class PublicationVoteSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PublicationVote
        fields = '__all__'


class PublicationVoteSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = PublicationVote
        exclude = ('publication', 'user')

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit publication votes from other users')
        return data
