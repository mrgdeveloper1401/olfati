from decouple import config
from kavenegar import KavenegarAPI


def send_sms_verify(phone, code):
    api_key = config("KAVENEGAR_API_KEY", cast=str)
    params = {
        'receptor': phone,
        'template': 'verify',
        'token': code,
        'type': 'sms',
    }
    api = KavenegarAPI(api_key)
    try:
        response = api.verify_lookup(params)
        return response
    except Exception as e:
        raise e
