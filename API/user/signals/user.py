import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from API.user.models.user import (AchievementMembership, Preferences,
                                  TagFollow, User, UserFriendship)
from services.achievement_helper import achievement_check_ws


@receiver(pre_save, sender=User)
def update_user(sender, instance, **kwargs):
    # Player Select
    # You change your avatar for first time
    user = User.objects.filter(id=instance.id).first()
    if user:
        if user.avatar == 'avatar-default.svg':
            achievement_check_ws(user, "player_select")


@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        # Create default user preferences
        Preferences.objects.create(user=instance)

        # It's dangerous to go alone, take this!
        # Register on page
        achievement_check_ws(instance, "its_dangerous_to_go_alone_take_this")

        from API.user.models.user import Title
        from API.user.models.user import TitleMembership
        noob_level_1_title, created = TitleMembership.objects.get_or_create(
            user=instance,
            title=Title.objects.get(slug="noob_level_1"),
            active=True,
        )

        from API.user.models.user import Border
        from API.user.models.user import BorderMembership
        noob_level_1_border, created = BorderMembership.objects.get_or_create(
            user=instance,
            border=Border.objects.get(slug="noob_level_1"),
            active=True,
        )

        aniversary = datetime.date(2018, 11, 30)
        week_delta = datetime.timedelta(days=8)

        if aniversary - week_delta <= datetime.date.today() <= aniversary + week_delta:
            # Pong
            # Register on page during the initial week or aniversary
            achievement_check_ws(instance, "pong")

            primera_oleada, created = BorderMembership.objects.get_or_create(
                user=instance,
                border=Border.objects.get(slug="primera_oleada"),
                active=True,
            )


@receiver(post_save, sender=AchievementMembership)
def new_achievement(sender, instance, **kwargs):
    achievements_obtained = len(AchievementMembership.objects.filter(user=instance.user))

    if achievements_obtained == 10:
        # Hazte con todos!
        # you obtain 10 achievements
        achievement_check_ws(instance.user, "hazte_con_todos")


@receiver(post_save, sender=UserFriendship)
def new_friendship(sender, instance, **kwargs):
    followed_user_total_followers = len(UserFriendship.objects.filter(friend=instance.friend))
    first_user_follow = len(UserFriendship.objects.filter(follower=instance.follower, follow=True))

    if first_user_follow == 1:
        # Get over here
        # You follow a user for the first time
        achievement_check_ws(instance.follower, "get_over_here")

    if followed_user_total_followers == 1:
        # Hello, Hello, Follow me, Ok
        # A user follows you for the first time
        achievement_check_ws(instance.friend, "hello_hello_follow_me_ok")

    elif followed_user_total_followers == 25:
        # ¡Conquistar el mundo!
        # 25 users follow you
        achievement_check_ws(instance.friend, "conquistar_el_mundo")

    elif followed_user_total_followers == 50:
        # Capitan Olimar
        # 50 users follow you
        achievement_check_ws(instance.friend, "capitan_olimar")

    elif followed_user_total_followers == 100:
        # WOLOLO
        # A hundred users follow you
        achievement_check_ws(instance.friend, "wololo")


@receiver(post_save, sender=TagFollow)
def new_tag_follow(sender, instance, **kwargs):
    first_tag_follow = len(TagFollow.objects.filter(follower=instance.follower))

    if first_tag_follow == 1:
        # vayas_donde_vayas_siempre_te_encontrare
        # You follow a tag for the first time
        achievement_check_ws(instance.follower, "vayas_donde_vayas_siempre_te_encontrare")
