from django.db import models
from django.contrib.auth.models import User

from so.constant import constant


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Website(TimestampedModel):
    title = models.CharField(max_length=64, verbose_name='标题', unique=True)
    sleep_seconds = models.IntegerField(default=3, verbose_name='爬取间隔时间')
    schedule_type = models.SmallIntegerField(
        choices=constant.SCHEDULE_CHOICES,
        default=constant.EVERY_DAY,
        verbose_name='爬取周期'
    )
    expire_seconds = models.IntegerField(
        default=0,
        verbose_name='页面过期时间'
    )

    class Meta:
        ordering = ['-id']


class WebsiteAllowedDomain(TimestampedModel):
    website = models.ForeignKey(Website)
    domain = models.CharField(max_length=256, verbose_name='主机名')

    class Meta:
        unique_together = ('website', 'domain')


class WebsiteUrlPattern(TimestampedModel):
    website = models.ForeignKey(Website)
    pattern_type = models.SmallIntegerField(choices=constant.URL_CHOICES)
    pattern = models.CharField(max_length=512)

    class Meta:
        unique_together = ('website', 'pattern_type', 'pattern')


class WebsiteSelector(TimestampedModel):
    website = models.ForeignKey(Website)
    key_name = models.CharField(max_length=24, verbose_name='名称')
    xpath = models.CharField(max_length=128)

    class Meta:
        unique_together = ('website', 'key_name')
