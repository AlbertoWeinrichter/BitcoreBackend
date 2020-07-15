from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField

from API.comments.models.comment import Comment
from API.general.models.general import CustomTag
from API.publication.models.publication import (ProsAndCons, Publication,
                                                PublicationImage,
                                                PublicationScore)
from API.user.serializers.user import ProfileUserSerializer
from API.votes.models.post_vote import PublicationVote


class PublicationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationScore
        fields = '__all__'


class ProsAndConsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProsAndCons
        fields = '__all__'


class PublicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImage
        fields = ('path', 'image_type')

    def to_representation(self, instance):
        data = super(PublicationImageSerializer, self).to_representation(instance)

        return data


class PublicationSerializer(serializers.ModelSerializer):
    genre_tags = TagListSerializerField()
    publisher_tags = TagListSerializerField()
    developer_tags = TagListSerializerField()
    tags = TagListSerializerField()
    images = PublicationImageSerializer(read_only=True, many=True)
    author = ProfileUserSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = (
            'id',
            'slug',
            'publication_type',
            'title',
            'subtitle',
            'game_release_name',
            'game_release_date',
            'publication_date',
            'masonry_snippet',
            'masonry_size',
            'genre_tags',
            'publisher_tags',
            'developer_tags',
            'tags',
            'author',
            'images',
        )

    def to_representation(self, instance):
        data = super(PublicationSerializer, self).to_representation(instance)
        comment_total = len(Comment.objects.filter(publication=instance.id))
        data.update({"comment_total": comment_total})

        up_votes = len(PublicationVote.objects.filter(publication=instance.id, value=1))
        data.update({"vote_total": up_votes})
        data.update({"publication_date": instance.publication_date.strftime("%Y-%m-%d %H:%M:%S")})

        # TODO: fix this in new version in production
        if data["masonry_size"] == 3:
            data["masonry_size"] = 2
        elif data["masonry_size"] == 4:
            data["masonry_size"] = 3

        return data


class PublicationDetailSerializer(serializers.ModelSerializer):
    title_tag = TagListSerializerField()
    genre_tags = TagListSerializerField()
    publisher_tags = TagListSerializerField()
    developer_tags = TagListSerializerField()
    review_platform_tags = TagListSerializerField()
    available_platform_tags = TagListSerializerField()

    tags = TagListSerializerField()
    scores = PublicationScoreSerializer(read_only=True, many=True)
    author = ProfileUserSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    pros_and_cons = ProsAndConsSerializer(read_only=True, many=True)

    class Meta:
        model = Publication
        fields = (
            'id',
            'slug',
            'publication_type',
            'title',
            'subtitle',
            'game_release_name',
            'game_release_date',
            'publication_date',
            'content',
            'title_tag',
            'genre_tags',
            'publisher_tags',
            'developer_tags',
            'review_platform_tags',
            'available_platform_tags',
            'tags',
            'scores',
            'author',
            'images',
            'pros_and_cons',
        )

    def to_representation(self, instance):
        data = super(PublicationDetailSerializer, self).to_representation(instance)
        user_vote = len(PublicationVote.objects.filter(user=self.context['request'].user.id, publication=instance))
        if user_vote > 0:
            voted = True
        else:
            voted = False
        up_votes = len(PublicationVote.objects.filter(publication=data["id"], value=1))
        down_votes = len(PublicationVote.objects.filter(publication=data["id"], value=-1))

        publication_votes = {
            "total": int(up_votes + down_votes),
            "voted": voted,
            "up": up_votes,
            "down": down_votes
        }
        data.update({"publication_votes": publication_votes})

        comment_total = len(Comment.objects.filter(publication=instance.id))
        data.update({"comment_total": comment_total})

        data.update({"title_tag": [{"name": t.name, "slug": t.slug} for t in
                                   CustomTag.objects.filter(name__in=data["title_tag"])]})
        data.update({"genre_tags": [{"name": t.name, "slug": t.slug} for t in
                                    CustomTag.objects.filter(name__in=data["genre_tags"])]})
        data.update({"publisher_tags": [{"name": t.name, "slug": t.slug} for t in
                                        CustomTag.objects.filter(name__in=data["publisher_tags"])]})
        data.update({"developer_tags": [{"name": t.name, "slug": t.slug} for t in
                                        CustomTag.objects.filter(name__in=data["developer_tags"])]})
        data.update({"review_platform_tags": [{"name": t.name, "slug": t.slug} for t in
                                              CustomTag.objects.filter(name__in=data["review_platform_tags"])]})
        data.update({"available_platform_tags": [{"name": t.name, "slug": t.slug} for t in
                                                 CustomTag.objects.filter(name__in=data["available_platform_tags"])]})
        data.update({"tags": [{"name": t.name, "slug": t.slug} for t in
                              CustomTag.objects.filter(name__in=data["tags"])]})
        return data
