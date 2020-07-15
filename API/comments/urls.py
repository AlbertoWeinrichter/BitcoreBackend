from django.conf.urls import url

from API.comments.views.comment import EditComment, LoadComment

from .views.comment import CreateComment

urlpatterns = [
    # Posts
    url(r'^comentarios/publication/(?P<slug>[\w-]+)$', LoadComment.as_view()),
    url(r'^comentarios/(?P<comment_id>[\d]+)$', EditComment.as_view()),
    url(r'^comentarios$', CreateComment.as_view()),
]
