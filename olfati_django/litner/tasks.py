from celery import shared_task
from firebase_admin import messaging

@shared_task
def send_notification_task(instance_id, device_tokens):
    from .models import NotificationModel  
    print("celery is worked")
    
    instance = NotificationModel.objects.get(pk=instance_id)
    message = messaging.Message(
        notification=messaging.Notification(
            title='سلام وقت بخیر',
            body=f'{instance} این سوالات اشتباه باسخ دادید'
        ),
        tokens=device_tokens,
    )

    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)