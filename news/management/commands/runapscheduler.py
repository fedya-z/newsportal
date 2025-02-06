import datetime
import logging
from django.core.mail import send_mail
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from project.news.models import Post, Subscription

logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)

    subscribers = Subscription.objects.all()
    for subscriber in subscribers:
        user_email = subscriber.user.email
        categories = subscriber.categories.all()

        posts = Post.objects.filter(category__in=categories, time_in_post__gte=last_week)

        if posts.exists():
            message = "Здравствуйте!\n\nВот список новых статей за последнюю неделю:\n\n"
            for post in posts:
                message += f"- {post.post_name}: http://127.0.0.1:8000/news/{post.id}\n"

            message += "\nС уважением,\nАдминистрация сайта."

            send_mail(
                subject="Еженедельная рассылка новостей",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )

            logger.info(f"Рассылка отправлена подписчику {user_email}")


def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def run():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_weekly_newsletter,
        trigger=CronTrigger(day_of_week="fri", hour=18, minute=0),
        id="send_weekly_newsletter",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Добавлена еженедельная рассылка новостей.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour=0, minute=0),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Добавлена ежедневная очистка старых задач.")

    scheduler.start()
    logger.info("Запущен планировщик задач.")