import json

from django.conf import settings
from django.http import HttpResponse
from froala_editor import S3


def get_signature(request):
    config = {
        # The name of your bucket.
        'bucket': 'bitcoregaming',

        # S3 region. If you are using the default us-east-1, it this can be ignored.
        'region': 'eu-west-1',

        # The folder where to upload the images.
        'keyStart': 'test',

        # File access.
        'acl': 'public-read',

        # AWS keys.
        'accessKey': settings.AWS_ACCESS_KEY,
        'secretKey': settings.AWS_SECRET_KEY
    }
    try:
        response = S3.getHash(config)
    except Exception as e:
        print(e)
        response = 1
    return HttpResponse(json.dumps(response), content_type="application/json")
