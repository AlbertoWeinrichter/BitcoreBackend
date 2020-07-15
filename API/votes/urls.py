from django.conf.urls import url

from .views.post_vote import (PostVoteDetail, PostVoteView,
                              PublicationVoteDetail, PublicationVoteView)

urlpatterns = [
    # Post votes
    url(r'^voto_post$', PostVoteView.as_view()),
    url(r'^voto_post/(?P<post_vote_id>[\d]+)$', PostVoteDetail.as_view()),

    url(r'^voto_publicacion$', PublicationVoteView.as_view()),
    url(r'^voto_publicacion/(?P<post_vote_id>[\d]+)$', PublicationVoteDetail.as_view()),
]
