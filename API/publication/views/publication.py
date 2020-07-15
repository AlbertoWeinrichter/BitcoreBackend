import logging
from datetime import datetime

from django.conf import settings
from django.db.models import Q
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework.views import APIView

from API.general.models.general import CustomTag
from API.patreon.models.patreon import PatreonUnlockedPublication
from API.publication.models.publication import Publication, PublicationImage
from API.publication.serializer.publication import (
    PublicationDetailSerializer, PublicationSerializer)

logger = logging.getLogger(__name__)


class PublicationAutocomplete(APIView):
    permission_classes = ()

    def get(self, request):
        search_string = request.query_params.get('search_string', None)

        if search_string:
            sqs = SearchQuerySet().models(Publication).autocomplete(title_auto=search_string)
            suggestions = [{"title": result.title, "slug": result.slug} for result in sqs[:5]]
        else:
            suggestions = []

        return Response({"results": suggestions})


class Publications(APIView):
    permission_classes = ()

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        """
        Publication view with cache
        """
        publications = Publication.objects.all().exclude(
            publication_type__in=["análisis_premium", "artículo_premium"]).distinct()

        # TODO: articulos not being correctly filtered
        if request.query_params.get('type') == "analisis":
            publication_types = ["análisis"]
            publications = publications.filter(publication_type__in=publication_types)
        elif request.query_params.get('type') == "articulos":
            publication_types = ["noticia", "artículo"]
            publications = publications.filter(publication_type__in=publication_types)

        publication_list = publications.order_by('-publication_date')
        if settings.BITCORE_SERVER_TYPE == "pro":
            now = datetime.today()
            publication_list = publication_list.exclude(publication_date__gte=now)

        total = len(publication_list)

        offset_start = request.query_params.get('offset_start')
        offset_end = request.query_params.get('offset_end')

        if request.query_params.get('type') == "masonry":
            rows = reorder_as_rows(publication_list[int(offset_start):int(offset_end)])
            publication_list = [item for sublist in rows for item in sublist]
        elif request.query_params.get('type') == "analisis":
            publication_list = publication_list[int(offset_start):int(offset_end)]
        elif request.query_params.get('type') == "articulos":
            publication_list = publication_list[int(offset_start):int(offset_end)]

        publication_serializer = PublicationSerializer(
            publication_list,
            many=True
        ).data

        return Response({"publications": publication_serializer,
                         "total": total})


class RelatedContent(APIView):
    permission_classes = ()

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, amount):
        """
        Load related content
        """
        if settings.BITCORE_SERVER_TYPE == "pro":
            now = datetime.today()
            publications = Publication.objects.exclude(publication_date__gte=now).exclude(
                publication_type__in=["análisis_premium", "análisis_premium"]).order_by('?')[:3]
        else:
            publications = Publication.objects.all().exclude(
                publication_type__in=["análisis_premium", "artículo_premium"]).order_by('?')[
                           :int(amount)]

        publication_serializer = PublicationSerializer(
            publications,
            many=True
        ).data
        return Response({"data": publication_serializer})


class PublicationSearch(APIView):
    permission_classes = ()

    def get(self, request):
        offset_start = request.query_params.get('offset_start')
        offset_end = request.query_params.get('offset_end')
        search_string = request.query_params.get('search_string', None)
        tag = request.query_params.get('tag', None)

        if tag:
            tag_id = CustomTag.objects.get(slug=tag).id

            publications = Publication.objects.filter(
                Q(genre_tags=tag_id) |
                Q(title_tag=tag_id) |
                Q(review_platform_tags=tag_id) |
                Q(available_platform_tags=tag_id) |
                Q(developer_tags=tag_id) |
                Q(publisher_tags=tag_id)
            ).exclude(publication_type__in=["análisis_premium", "artículo_premium"]).distinct()

            if settings.BITCORE_SERVER_TYPE == "pro":
                now = datetime.today()
                publications = publications.exclude(publication_date__gte=now)

            publication_serializer = PublicationSerializer(
                publications[int(offset_start):int(offset_end)],
                many=True
            ).data

        else:
            sqs = SearchQuerySet().models(Publication).autocomplete(title_auto=search_string)
            suggestions = [result.slug for result in sqs]

            publications = Publication.objects.filter(slug__in=suggestions)

            if settings.BITCORE_SERVER_TYPE == "pro":
                now = datetime.today()
                publications = publications.exclude(publication_date__gte=now)

            publication_serializer = PublicationSerializer(
                publications,
                many=True
            ).data

        total = len(publications)

        return Response({"publications": publication_serializer,
                         "total": total})


def reorder_as_rows(publications):
    ordered_publications = []
    already_seen = []
    rows = 0
    try:
        for i, p in enumerate(publications):
            if p.masonry_size == 1 and p not in already_seen:
                next_small = publications.index(
                    [p for p in publications[i + 1:] if
                     p.masonry_size == 1 and p not in already_seen][0])
                already_seen.append(publications[i])
                already_seen.append(publications[next_small])
                ordered_publications.append([publications[i], publications[next_small]])
                rows += 1
            elif p not in already_seen:
                ordered_publications.append([publications[i]])
                rows += 1
            elif rows >= len(publications):
                break
        return ordered_publications
    except Exception as e:
        logger.error(e)
        return ordered_publications
        pass


class NewPublications(APIView):
    permission_classes = ()

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        """
        Load last publications
        """
        if settings.BITCORE_SERVER_TYPE == "pro":
            now = datetime.today()
            publication = Publication.objects.exclude(publication_date__gte=now).exclude(
                publication_type__in=["análisis_premium", "artículo_premium"]).order_by(
                '-publication_date')[:6]
        else:
            publication = Publication.objects.exclude(
                publication_type__in=["análisis_premium", "artículo_premium"]).order_by(
                '-publication_date')[:6]

        publication_serializer = PublicationSerializer(publication, many=True).data

        return Response({"publications": publication_serializer})


class PublicationDetail(APIView):
    permission_classes = ()

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, slug):
        publication = Publication.objects.get(slug=slug)
        publication_serializer = PublicationDetailSerializer(publication,
                                                             context={'request': request}).data

        related_amount = 3

        if settings.BITCORE_SERVER_TYPE == "pro":
            now = datetime.today()
            related_articles = Publication.objects.exclude(publication_date__gte=now).exclude(
                publication_type__in=["análisis_premium", "artículo_premium"]).order_by('?')[
                               :int(related_amount)]
        else:
            related_articles = Publication.objects.all().exclude(
                publication_type__in=["análisis_premium", "artículo_premium"]).order_by('?')[
                               :int(related_amount)]

        related_serializer = PublicationSerializer(
            related_articles,
            many=True
        ).data

        patreon_locked = PatreonUnlockedPublication.objects.filter(publication=publication).first()
        if patreon_locked:
            if patreon_locked.minimum_level_needed > request.user.patreon_level:
                return 1

        return Response(
            {"publication": publication_serializer,
             "related": related_serializer
             }
        )


def media_to_dic(publication):
    media_items = PublicationImage.objects.filter(publication=publication)
    media_dic = {}

    [media_dic.update({i.image_type: i.path}) for i in media_items]

    return media_dic
