from django.db import models


class ExamEnums(models.TextChoices):
    zero = "zero", "0"
    one = "one", "1"
    two = "two", "2"
    three = "three", "3"
    four = "four", "4"
