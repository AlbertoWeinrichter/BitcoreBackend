from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.patreon.models.patreon import (PatreonImage,
                                        PatreonUnlockedPublication, Survey)
from API.patreon.serializer.patreon import (PatreonImageSerializer,
                                            PatreonSurveySerializer)
from API.publication.serializer.publication import PublicationSerializer
from API.user.models.user import User


def slugify(term):
    slug = term.replace(' ', '_').replace('.', '_').replace(',', '_').lower()

    return slug


class LoadUnlocked(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Load Patreon content unlocked by the user
        """
        user = get_object_or_404(User, username=request.user.username)
        news = PatreonUnlockedPublication.objects.filter(
            publication__publication_type="artículo_premium",
            minimum_level_needed__lte=user.patreon_level)

        serialized_news = [n.publication.slug for n in news]
        reviews = PatreonUnlockedPublication.objects.filter(
            publication__publication_type="análisis_premium",
            minimum_level_needed__lte=user.patreon_level)

        serialized_reviews = [r.publication.slug for r in reviews]

        surveys = Survey.objects.filter(minimum_level_needed__lte=user.patreon_level)
        serialized_surveys = [s.id for s in surveys]

        images = PatreonImage.objects.filter(minimum_level_needed__lte=user.patreon_level)
        serialized_images = [{"id": i.id,
                              "thumbnail": i.thumbnail,
                              "url": i.url} for i in images]

        unlocked = {
            "news": serialized_news,
            "reviews": serialized_reviews,
            "surveys": serialized_surveys,
            "images": serialized_images
        }

        news = PatreonUnlockedPublication.objects.filter(publication__publication_type="artículo_premium")
        serialized_news = PublicationSerializer([n.publication for n in news], many=True).data

        reviews = PatreonUnlockedPublication.objects.filter(publication__publication_type="análisis_premium")
        serialized_reviews = PublicationSerializer([r.publication for r in reviews], many=True).data

        surveys = Survey.objects.all()
        serialized_surveys = PatreonSurveySerializer(surveys, many=True).data

        images = PatreonImage.objects.all()
        serialized_images = PatreonImageSerializer(images, many=True).data

        all = {
            "news": serialized_news,
            "reviews": serialized_reviews,
            "surveys": serialized_surveys,
            "images": serialized_images
        }

        response = {
            "all": all,
            "unlocked": unlocked
        }

        return Response(response, status=status.HTTP_200_OK)


class LoadAll(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        """
        Load all Patreon content
        """

        news = PatreonUnlockedPublication.objects.filter(publication__publication_type="artículo_premium")
        serialized_news = PublicationSerializer([n.publication for n in news], many=True).data

        reviews = PatreonUnlockedPublication.objects.filter(publication__publication_type="análisis_premium")
        serialized_reviews = PublicationSerializer([r.publication for r in reviews], many=True).data

        surveys = Survey.objects.all()
        serialized_surveys = PatreonSurveySerializer(surveys, many=True).data

        images = PatreonImage.objects.all()
        serialized_images = PatreonImageSerializer(images, many=True).data

        response = {
            "news": serialized_news,
            "reviews": serialized_reviews,
            "surveys": serialized_surveys,
            "images": serialized_images
        }

        return Response(response, status=status.HTTP_200_OK)
