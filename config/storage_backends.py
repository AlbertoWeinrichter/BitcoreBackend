from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import mimetypes


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False

    # def _save(self, name, content):
    #     cleaned_name = self._clean_name(name)
    #     name = self._normalize_name(cleaned_name)
    #     parameters = self.object_parameters.copy()
    #     _type, encoding = mimetypes.guess_type(name)
    #     content_type = getattr(content, 'content_type', None)
    #     content_type = content_type or _type or self.default_content_type
    #
    #     # setting the content_type in the key object is not enough.
    #     parameters.update({'ContentType': content_type})
    #
    #     if self.gzip and content_type in self.gzip_content_types:
    #         content = self._compress_content(content)
    #         parameters.update({'ContentEncoding': 'gzip'})
    #     elif encoding:
    #         # If the content already has a particular encoding, set it
    #         parameters.update({'ContentEncoding': encoding})
    #
    #     encoded_name = self._encode_name(name)
    #     obj = self.bucket.Object(encoded_name)
    #     if self.preload_metadata:
    #         self._entries[encoded_name] = obj
    #
    #     # If both `name` and `content.name` are empty or None, your request
    #     # can be rejected with `XAmzContentSHA256Mismatch` error, because in
    #     # `django.core.files.storage.Storage.save` method your file-like object
    #     # will be wrapped in `django.core.files.File` if no `chunks` method
    #     # provided. `File.__bool__`  method is Django-specific and depends on
    #     # file name, for this reason`botocore.handlers.calculate_md5` can fail
    #     # even if wrapped file-like object exists. To avoid Django-specific
    #     # logic, pass internal file-like object if `content` is `File`
    #     # class instance.
    #     if isinstance(content, File):
    #         content = content.file


# This will transform to webp

# from PIL import Image
#
# image_old = 'e:\\1.png'
# image_new = 'e:\\1.webp'
#
# im = Image.open(image_old)
# im.save(image_new, format="WebP", lossless=True)

# Maybe check this article
# https://github.com/gkuhn1/django-admin-multiupload
