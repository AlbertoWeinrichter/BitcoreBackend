import logging

from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.general.models.general import Ad, CustomTag, Quote
from API.general.serializer.general import (ContactFormCreateSerializer,
                                            PublicitySerializer,
                                            QuoteSerializer, TagSerializer)
from services.achievement_helper import achievement_check_ws

logger = logging.getLogger(__name__)


def slugify(term):
    slug = term.replace(' ', '_').replace('.', '_').replace(',', '_').lower()

    return slug


class FixDB(APIView):
    permission_classes = ()

    def get(self, request):
        try:
            from API.publication.models.publication import PublicationImage
            from API.publication.models.publication import Publication
            from API.releases.models.release import ReleaseImage
            from API.user.models.user import User

            # for p in Publication.objects.all():
            #     print(p.content)
            #     p.content = p.content.replace('articulos/', 'publicacion/')
            #     p.save()

            # for p in Publication.objects.all():
            #     images = PublicationImage.objects.filter(publication=p)
            #     if len(images) == 4:
            #         image = PublicationImage.objects.create(publication=p, image_type="rrss", path=images[1].path)
            #         print(image)
            #
            # for p in PublicationImage.objects.all():
            #     if p.image_type == "rrss":
            #         p.path = p.publication.slug + "_search_500x300.png".replace("analisis_", "")
            #         p.save()
            for p in PublicationImage.objects.all():
                print(p.path)
                p.path = p.path.name.replace('"/media/', '"https://bitcoregaming.s3.amazonaws.com/media/')
                p.save()

            # for p in PublicationImage.objects.all():
            #     print(p.path.name)
            #     # MAGIC! Do not try to fix this
            #     if p.publication.publication_type == "noticia" and "noticias" in p.path.name:
            #         wii = True if len(p.path.name.split("/")) > 1 else False
            #         if wii:
            #             p.path.name = p.path.name.split("/")[3]
            #             p.save()
            #             print(p.path.name)

            #     wii = p.path.name.split("/")[2] if 2 < len(p.path.name.split("/")) else None
            #     if wii:
            #         p.path.name = p.path.name.split("/")[2]
            #         p.save()
            #         print(p.path.name)
            #
            # for p in ReleaseImage.objects.all():
            #     p.path.name = p.path.name.split("/")[1]
            #     p.save()
            #     print(p.path.name)
            #
            # users = User.objects.all()
            # for u in users:
            #     print(u.username)
            #     u.avatar = "https://s3.eu-central-1.amazonaws.com/bitcoregaming/avatars/" + u.avatar
            #     u.avatar_cropped = "https://s3.eu-central-1.amazonaws.com//bitcoregaming/avatars/" + u.avatar_cropped
            #     u.save()
            #
            # for p in Publication.objects.all():
            #     p.content.replace("bitcoregaming.com/articulos/", "bitcoregaming.com/publicacion/")
            #     if p.publication_type == "curiosidad" or p.publication_type == "opinion":
            #         print(p.publication_type)
            #         p.publication_type = 'noticia'
            #     p.save()

            return Response({"status": "Success"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(e)
            return Response({"status": "Warning"}, status=status.HTTP_304_NOT_MODIFIED)


class AcceptManifesto(APIView):
    permission_classes = ()

    def get(self, request):
        try:
            achievement_check_ws(request.user, "manda_cuando_hayas_aprendido_a_obedecer")

            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(e)
            return Response({"status": "Warning"}, status=status.HTTP_304_NOT_MODIFIED)


class ContactForm(APIView):
    permission_classes = ()

    @staticmethod
    def post(request):
        serializer = ContactFormCreateSerializer(data=request.data['formData'],
                                                 context={'request': request})

        if serializer.is_valid():
            serializer.save()

            from django.core.mail import send_mail

            send_mail(
                request.data["formData"]["subject"],
                "USUARIO:" + request.data["formData"]["username"] + "\n MENSAJE:" +
                request.data["formData"][
                    "content"] + "\n CORREO:" + request.data["formData"]["email"],
                'bitmail@bitcoregaming.com.com',
                ['bitcore.rrss@gmail.com'],
                fail_silently=False,
            )

            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuoteView(APIView):
    permission_classes = ()

    def get(self, request):
        quote = Quote.objects.order_by('?').first()
        quote_serializer = QuoteSerializer(quote, context={'request': request}).data

        return Response({"quote": quote_serializer})


class PublicityView(APIView):
    permission_classes = ()

    def get(self, request, ad_type):
        serialized_publicity = PublicitySerializer(
            Ad.objects.filter(ad_type=ad_type).order_by('?').first()).data

        return Response(serialized_publicity)


class TagDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        tag_name = request.data["tag_name"]
        tag = get_object_or_404(CustomTag, slug=tag_name)

        return Response(TagSerializer(tag, context={'request': request}).data)


class TagAutocomplete(APIView):
    permission_classes = ()

    def get(self, request):
        search_term = request.query_params.get('search_term')
        sqs = SearchQuerySet().autocomplete(username=search_term)
        results = [result.object for result in sqs]

        return Response({"results": results})
