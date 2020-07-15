from django.db import models


# General notification to reference to specific one
class Notification(models.Model):
    types = [
        ('post_vote', 'post vote'),  # Someone voted your comment
        ('user_follow', 'user follow'),  # Someone followed you
        ('user_post', 'new user post'),  # Someone you followed commented on an article
        ('tag_content', 'new tag content'),  # An article related to a tag you follow has been published
        ('private_message', 'new private message'),  # You have a new private message
        ('achievement', 'new achievement')
    ]
    notification_type = models.CharField(max_length=999, choices=types)

    # Shared fields
    timestamp = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=True)
    owner = models.ForeignKey('user.user', related_name="owner", blank=True, null=True, on_delete=models.CASCADE)
    notification_message = models.CharField(max_length=999)

    # Depending on notification type
    sender = models.ForeignKey('user.user', related_name="sender", blank=True, null=True, on_delete=models.CASCADE)
    voted_post = models.ForeignKey('comments.comment', related_name="voted_post", blank=True, null=True,
                                   on_delete=models.CASCADE)
    new_post = models.ForeignKey('comments.comment', related_name="new_post", blank=True, null=True,
                                 on_delete=models.CASCADE)
    new_publication = models.ForeignKey('publication.publication', related_name="new_publication", blank=True,
                                        null=True, on_delete=models.CASCADE)
    new_achievement = models.ForeignKey('user.AchievementMembership', related_name="new_achievement", blank=True,
                                        null=True, on_delete=models.CASCADE)
