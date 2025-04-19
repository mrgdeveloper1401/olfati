from rest_framework import exceptions, status
from kavenegar import KavenegarAPI
from urllib3.exceptions import HTTPError as Urllib3HTTPError, MaxRetryError, NameResolutionError
from requests.exceptions import ConnectionError, Timeout
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
    except (Urllib3HTTPError, MaxRetryError, NameResolutionError, ConnectionError) as e:
        raise exceptions.APIException(
            detail="مشکل در اتصال به اینترنت یا سرویس پیامکی",
            code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        raise exceptions.APIException(
            detail="خطای داخلی سرویس",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
