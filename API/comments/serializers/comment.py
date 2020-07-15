from rest_framework import serializers

from API.comments.models.comment import Comment
from API.publication.models.publication import Publication
from API.user.serializers.user import ProfileUserSerializer
from API.votes.models.post_vote import PostVote
from API.votes.serializers.post_vote import PostVoteSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentTreeSerializer(serializers.ModelSerializer):
    post_votes = PostVoteSerializer(many=True, read_only=True)
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'timestamp',
            'body',
            'post_votes',
            'children',
        )

    def to_representation(self, instance):
        data = super(CommentTreeSerializer, self).to_representation(instance)
        voted = False
        up_votes = len(PostVote.objects.filter(post=data["id"], value=1))
        down_votes = len(PostVote.objects.filter(post=data["id"], value=-1))

        publication_votes = {
            "voted": voted,
            "up": up_votes,
            "down": down_votes
        }
        data.update({"post_votes": publication_votes})

        user_profile = ProfileUserSerializer(instance.user).data
        data.update({"user": user_profile})

        return data


class CommentSerializer(serializers.ModelSerializer):
    comment_reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)

    def save(self):
        user = self.context["request"].user
        self.validated_data.update({"user": user})

        publication = Publication.objects.get(id=self.data["publication"])
        self.validated_data.update({"publication": publication})

        if self.data["parent"]:
            parent = Comment.objects.get(id=self.data["parent"])
        else:
            parent = None
        self.validated_data.update({"parent": parent})
        self.create(self.validated_data)


class CommentSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit comments from other users')
        return data
