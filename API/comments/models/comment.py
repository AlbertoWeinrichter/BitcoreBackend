from django.db import models

from API.general.created_modified import CreatedModified
from API.publication.models.publication import Publication


class Comment(CreatedModified):
    user = models.ForeignKey('user.user', related_name="user", on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name="children", blank=True, null=True, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    total_votes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user.username + " " + str(self.created_date.date())

    def increase_vote_count(self):
        self.total_votes = self.total_votes + 1


# ALWAYS SKIP ISORT AND ALWAYS IMPORT AT THE END OF MODELS OR SIGNALSGIVE A CIRCULAR DEPENDENCY ERROR
from API.comments.signals.comment import new_comment # noqa isort:skip
