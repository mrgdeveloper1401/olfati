from celery import shared_task
from django.apps import apps
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .notification import send_push_notification

@shared_task
def update_is_correctt():
    UserQuestionAnswerCount = apps.get_model('litner', 'UserQuestionAnswerCount')
    
    three_days_ago = timezone.now() - timedelta(days=3)
    UserQuestionAnswerCount.objects.filter(
        is_correctt=True,
        answered_at__lte=three_days_ago
    ).update(is_correctt=False)


@shared_task
def send_notification_task(token, title, body):
    send_push_notification(token, title, body)




