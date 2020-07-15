from django.db.models.signals import post_save
from django.dispatch import receiver

from API.comments.models.comment import Comment
from API.votes.models.post_vote import PostVote
from services.achievement_helper import achievement_check_ws


@receiver(post_save, sender=PostVote)
def new_post_vote(sender, instance, **kwargs):
    user_to_send = instance.post.user

    # ################################################### #
    # ### CHECK NUMBER OF LIKES IN INDIVIDUAL COMMENT ### #
    # ################################################### #
    if instance.post.total_votes == 1:
        # ACHIEVEMENT: 1 UP
        achievement_check_ws(user_to_send, "1up")

    elif instance.post.total_votes == 25:
        # ACHIEVEMENT: ¡ES SUPER EFECTIVO!
        achievement_check_ws(user_to_send, "es_super_efectivo")

    elif instance.post.total_votes == 50:
        # ACHIEVEMENT: BIG BOSS
        achievement_check_ws(user_to_send, "big_boss")

    elif instance.post.total_votes == 100:
        # ACHIEVEMENT: MASTER CHIEF
        achievement_check_ws(user_to_send, "master_chief")

    elif instance.post.total_votes == 250:
        # ACHIEVEMENT: JACKPOT!
        achievement_check_ws(user_to_send, "jackpot")

    elif instance.post.total_votes == 250:
        # ACHIEVEMENT: HAIL TO THE KING, BABY!
        achievement_check_ws(user_to_send, "hail_to_the_king_baby")

    # ###################################################### #
    # ### CHECK NUMBER OF COMMENTS WITH AT LEST ONE LIKE ### #
    # ###################################################### #
    total_voted_posts = len(Comment.objects.filter(total_votes__gte=0))
    if total_voted_posts == 25:
        # GO GO GO!
        achievement_check_ws(user_to_send, "go_go_go")

    elif total_voted_posts == 50:
        # Nada es verdad, toudo esta permitido
        achievement_check_ws(user_to_send, "nada_es_verdad_todo_esta_permitido")

    elif total_voted_posts == 100:
        # Rosebud
        achievement_check_ws(user_to_send, "rosebud")

    elif total_voted_posts == 250:
        # Ya no hay noticias, solo propaganda
        achievement_check_ws(user_to_send, "ya_no_hay_noticias_solo_propaganda")

    elif total_voted_posts == 250:
        # Hey, listen!
        achievement_check_ws(user_to_send, "hey_listen")
