from kavenegar import KavenegarAPI
from decouple import config


def send_sms_verify(phone, code):
    api_key = config("KAVENEGAR_API_KEY", cast=str)
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
