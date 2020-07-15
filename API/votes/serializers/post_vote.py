from rest_framework import serializers

from API.votes.models.post_vote import PostVote


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = '__all__'


class PostVoteSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostVote
        fields = '__all__'

    def create(self, validated_data):
        validated_data["post"].total_votes += 1
        validated_data["post"].save()
        return PostVote.objects.create(**validated_data)


class PostVoteSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        exclude = ('post', 'user')

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit post votes from other users')
        return data
