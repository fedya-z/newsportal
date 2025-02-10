from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, User
from django.utils import timezone

@shared_task
def send_weekly_newsletter():
    last_week = timezone.now() - timezone.timedelta(weeks=1)
    posts = Post.objects.filter(time_in_post__gte=last_week)

    users = User.objects.all()

    subject = "Еженедельная рассылка новостей"
    message = "Вот самые последние новости за неделю:\n\n"

    for post in posts:
        message += f"- {post.post_name}: {post.text_post}\n"

    for user in users:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )