from __future__ import unicode_literals

import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _
from django.db.utils import IntegrityError
from rest_framework import HTTP_HEADER_ENCODING

from API.user.exceptions import AuthenticationFailed, InvalidToken

logger = logging.getLogger(__name__)
User = get_user_model()


class BitcoreTokenBackend:
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a cookie.
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return (AnonymousUser(), False)

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return (AnonymousUser(), False)

        validated_token = self.get_validated_token(raw_token)
        if validated_token is None:
            return (AnonymousUser(), False)

        return (self.get_user(validated_token), True)

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token.get("user_id").split("|")[1]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            if User.objects.filter(auth_id=user_id).exists():
                user = User.objects.get(auth_id=user_id)
                return user
            else:
                user, created = User.objects.get_or_create(
                    auth_id=user_id,
                )
                if created:
                    user.username = validated_token["username"].replace(".", "")
                    user.avatar = validated_token["picture"]
                    user.avatar_cropped = validated_token["picture"]
                    user.save()

                return user
        except Exception as e:
            logger.error(e)

    def get_validated_token(self, raw_token):
        """
        Validates against auth0 public key to token has not been tampered with
        """
        try:
            payload = jwt.decode(raw_token, settings.PUBLIC_KEY, algorithms=['RS256'],
                                 audience=settings.AUTH0_CLIENT_ID)

            return {'username': payload['nickname'],
                    'first_name': payload['name'],
                    'picture': payload['picture'],
                    'user_id': payload['sub']}

        except jwt.ExpiredSignatureError as e:
            logger.error(e)
            return None

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """

        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if str(parts[0], 'utf-8') not in ['Token', ]:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _('Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        try:
            header = request.META.get('HTTP_AUTHORIZATION', None)

            if isinstance(header, str):
                header = header.encode(HTTP_HEADER_ENCODING)
            else:
                return None

            return header
        except Exception as e:
            logger.error(e)
            return None
