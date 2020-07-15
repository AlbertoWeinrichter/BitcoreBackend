from django.conf.urls import url

from API.releases.views.release import LoadReleases

urlpatterns = [
    url(r'^releases$', LoadReleases.as_view()),
]
