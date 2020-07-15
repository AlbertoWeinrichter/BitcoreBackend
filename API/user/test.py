from django.test import TestCase

from API.user.models.user import (Achievement, AchievementMembership, Border,
                                  BorderMembership, Title, TitleMembership,
                                  User)


class AnimalTestCase(TestCase):

    def setUp(self):
        title = Title.objects.create(
            name="test_title",
            slug="noob_level_1",
            description="test description",
        )

        Achievement.objects.create(
            title=title,
            name="Its dangeours to go alone take this",
            slug="its_dangerous_to_go_alone_take_this",
            category="wii",
            weight=1,
            description="wii",
            game="wii",
            active=True
        )

        border = Border.objects.create(
            title=title,
            name="test border",
            slug="noob_level_1",
            description="test description",
        )

        user = User.objects.create(
            auth_id="123456789",
            username="test_user",
            avatar="a_url.png",
            avatar_cropped="a_url.png",
        )

        TitleMembership.objects.create(
            user=user,
            title=title,
            active=True,
        )

        BorderMembership.objects.create(
            user=user,
            border=border,
            active=True,
        )

    def test_user_is_created(self):
        user = User.objects.get(username="test_user")

        self.assertEqual(user.username, 'test_user')

    def test_initial_achievement(self):
        user = User.objects.get(username="test_user")

        achievement = AchievementMembership.objects.create(
            user=user,
            achievement=Achievement.objects.get(slug="its_dangerous_to_go_alone_take_this")
        )

        self.assertEqual(achievement.achievement.slug, "its_dangerous_to_go_alone_take_this")
