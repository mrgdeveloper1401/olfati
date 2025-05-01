from kavenegar import KavenegarAPI
from decouple import config


api_key = config("KAVENEGAR_API_KEY", cast=str)


def send_sms_verify(phone, code):
    params = {
        'receptor': phone,
        'template': 'verify',
        'token': code,
        'type': 'sms',
    }
    try:
        api = KavenegarAPI(api_key)
        response = api.verify_lookup(params)
        return response
    except Exception as e:
        raise e


def send_successfully_sms(phone, text):
    params = {
        'receptor': phone,
        'template': 'verify',
        'token': code,
        'type': 'sms',
    }