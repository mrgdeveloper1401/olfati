import logging

from celery import shared_task
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from .models import LitnerKarNameDBModel
from firebase_admin import messaging
from accounts.models import UserModel

logger = logging.getLogger(__name__)


@shared_task
def update_is_correctt():
    three_days_ago = timezone.now() - timedelta(days=3)
    UserQuestionAnswerCount = apps.get_model('litner', 'UserQuestionAnswerCount')
    karnamedb = apps.get_model('litner', 'LitnerKarNameDBModel')
    karnamedb.objects.filter(is_correct=True, answered_at__lte=three_days_ago).update(is_correct=False)

    UserQuestionAnswerCount.objects.filter(
        is_correctt=True,
        answered_at__lte=three_days_ago
    ).update(is_correctt=False)


# @shared_task
# def send_notification_task(token, title, body):
# send_push_notification(token, title, body)


@shared_task
def send_notification_task(fcm_token, title, body):
    try:
        notification = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=fcm_token
        )
        response = messaging.send(notification)
        logger.info(f"Notification sent successfully: {response}")
    except Exception as e:
        logger.error(f'Error sending notification \nException: {e}', exc_info=True)
