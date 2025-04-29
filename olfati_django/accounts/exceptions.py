from rest_framework import exceptions, status


class UserNotFound(exceptions.APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = "user not found"
    default_code = "user_not_found"
