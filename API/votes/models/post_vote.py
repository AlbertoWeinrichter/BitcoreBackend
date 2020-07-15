from django.db import models

from API.comments.models.comment import Comment
from API.publication.models.publication import Publication
from API.votes.models.vote import Vote


class PostVote(Vote):
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'post_votes'
        unique_together = ('post', 'user')

    def __str__(self):
        return f'post: {self.post.id} - value: {self.value}'


class PublicationVote(Vote):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'publication_votes'
        unique_together = ('publication', 'user')

    def __str__(self):
        return f'post: {self.publication.id} - value: {self.value}'
