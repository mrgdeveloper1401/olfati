from celery import shared_task
from firebase_admin import messaging
import logging

#@shared_task
#def send_notification_task(instance_id, device_tokens):
   # from .models import NotificationModel  
   # print("celery is worked")
    
   # instance = NotificationModel.objects.get(pk=instance_id)
   # message = messaging.Message(
     #   notification=messaging.Notification(
      #      title='سلام وقت بخیر',
    #        body=f'{instance} این سوالات اشتباه باسخ دادید'
      #  ),
   #     tokens=device_tokens,
   # )

   # response = messaging.send_multicast(message)
   # print('Successfully sent message:', response)

logger = logging.getLogger(__name__)

@shared_task
def send_notification_task(instance_id, device_tokens):
    from .models import NotificationModel  
    try:
        instance = NotificationModel.objects.get(pk=instance_id)
        message = messaging.Message(
            notification=messaging.Notification(
                title='سلام وقت بخیر',
                body=f'{instance} این سوالات اشتباه باسخ دادید'
            ),
            tokens=device_tokens,
        )

        response = messaging.send_multicast(message)
        logger.info('Successfully sent message: %s', response)

    except NotificationModel.DoesNotExist:
        logger.error("NotificationModel with id %d does not exist.", instance_id)
    except Exception as e:
        logger.error("Error sending notification: %s", str(e))