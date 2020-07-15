from django.conf.urls import url

from API.patreon.views.patreon import LoadAll, LoadUnlocked

urlpatterns = [
    url(r'^fetch_unlocked_patreon', LoadUnlocked.as_view()),
    url(r'^fetch_all_patreon$', LoadAll.as_view())
]
