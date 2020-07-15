from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField

from API.releases.models.release import Release, ReleaseImage


class ReleaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseImage
        fields = ("path",)

    def to_representation(self, instance):
        data = super(ReleaseImageSerializer, self).to_representation(instance)

        data.update({"path": instance.path.name})

        return data


class ReleaseSerializer(serializers.ModelSerializer):
    important_tags = TagListSerializerField()
    other_tags = TagListSerializerField()

    class Meta:
        model = Release
        fields = (
            'id',
            'release_date',
            'release_type',
            'title',
            'important_tags',
            'other_tags',
            'snippet',
            'description',
            'video',
            'external_link',
            'review_link'
        )

    def to_representation(self, instance):
        data = super(ReleaseSerializer, self).to_representation(instance)

        try:
            main_image = ReleaseImage.objects.get(
                release=instance.id,
                image_type="main"
            )
            data.update({"main_image": main_image.path.name})

            thumbnail_image = ReleaseImage.objects.get(
                release=instance.id,
                image_type="main"
            )
            data.update({"thumbnail": thumbnail_image.path.name})

            images = ReleaseImage.objects.filter(
                release=instance.id,
                image_type="gallery"
            )
            serialized_images = ReleaseImageSerializer(images, many=True).data
            data.update({"images": serialized_images})

            if instance.review_link:
                data.update({"review_link": instance.review_link.slug})

            return data
        except Exception as e:
            print(e)
