import firebase_admin
from firebase_admin import credentials, messaging
from django.utils import timezone
from datetime import timedelta
from .tasks import send_notification_task

cred = credentials.Certificate('litner/firebase-key.json')
firebase_admin.initialize_app(cred)


def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)


def schedule_notification(user, incorrect_answers, exam):
    """
    Schedule notifications for the user:
    1. After 24 hours, notify the user about their wrong answers.
    2. After 3 days, notify the user that they now have access to the exam again.
    """
    # 24-hour notification
    wrong_answer_count = len(incorrect_answers)
    notification_time_24hrs = timezone.now() + timedelta(hours=24)
    message_24hrs = f"You had {wrong_answer_count} wrong answers in your last exam."
    send_notification_task.apply_async(args=[user.id, message_24hrs], eta=notification_time_24hrs)

    # 3-day notification (72 hours)
    notification_time_3days = timezone.now() + timedelta(days=3)
    message_3days = "You now have access to your exam again."
    send_notification_task.apply_async(args=[user.id, message_3days], eta=notification_time_3days)
