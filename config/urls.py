from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()

urlpatterns = [
    # API
    url(r'^api/', include('API.user.urls')),
    url(r'^api/', include('API.comments.urls')),
    url(r'^api/', include('API.votes.urls')),
    url(r'^api/', include('API.releases.urls')),
    url(r'^api/', include('API.publication.urls')),
    url(r'^api/', include('API.notifications.urls')),
    url(r'^api/', include('API.general.urls')),
    url(r'^api/', include('API.chat.urls')),
    url(r'^api/', include('API.patreon.urls')),

    # Admin
    url(r'^api/docs/', include_docs_urls(title='My API title')),
    url(r'^admin/', admin.site.urls),

    # WYSIWYG
    url(r'^api/froala_editor/', include('froala_editor.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
