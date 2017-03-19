from django.db import models
from django.contrib.auth.models import User

from so.constant import constant


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Website(TimestampedModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=64)
    sleep_seconds = models.IntegerField()
    schedule_type = models.SmallIntegerField(choices=constant.SCHEDULE_CHOICES,
                                             default=constant.EVERY_DAY)
    expire_seconds = models.IntegerField()


class WebsiteAllowedDomain(TimestampedModel):
    website = models.ForeignKey(Website)
    domain = models.CharField(max_length=256)


class WebsiteUrlPattern(TimestampedModel):
    pattern_type = models.SmallIntegerField(choices=constant.URL_CHOICES)
    pattern = models.CharField(max_length=512)


class WebsiteSelector(TimestampedModel):
    key_name = models.CharField(max_length=24)
    xpath = models.CharField(max_length=128)
