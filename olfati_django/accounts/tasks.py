from celery import shared_task
from utils.sed_code import send_sms_verify


@shared_task()
def send_async_otp_code(phone, code):
    send_sms_verify(phone, code)
