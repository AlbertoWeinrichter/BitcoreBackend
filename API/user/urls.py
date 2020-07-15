from django.conf.urls import url

from API.user.views.social import FollowTag, FollowUser
from API.user.views.user import (AchievementList, Login, NewUsersView,
                                 SubscriptionView, UpdatePreferences,
                                 UpdateUserView, UserAutocomplete, UserDetail,
                                 UserTutorial)

urlpatterns = [
    # Users
    url(r'^login$', Login.as_view()),
    url(r'^tutorial', UserTutorial.as_view()),
    url(r'^actualizar_usuario', UpdateUserView.as_view()),
    url(r'^actualizar_preferencias', UpdatePreferences.as_view()),
    url(r'^listado_achievements', AchievementList.as_view()),
    url(r'^usuarios/(?P<username>[\w-]+)$', UserDetail.as_view()),
    url(r'^new_users', NewUsersView.as_view()),
    url(r'^user_autocomplete$', UserAutocomplete.as_view()),
    url(r'^tutorial$', UserTutorial.as_view()),

    # Social
    url(r'^seguir_usuario', FollowUser.as_view()),
    url(r'^seguir_etiqueta', FollowTag.as_view()),
    url(r'^subscripcion/(?P<username>[\w-]+)$', SubscriptionView.as_view()),
]
