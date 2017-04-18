from django.db.models.signals import post_save

from so.models import Website, WebsiteUrlPattern, WebsiteSelector
from so.constant import constant


def auto_create_url_pattern(sender, instance, created, *args, **kwargs):
    if not created:
        return
    WebsiteUrlPattern.objects.create(
        website=instance,
        pattern_type=constant.URL_PARSE,
        pattern='.*'
    )
    WebsiteUrlPattern.objects.create(
        website=instance,
        pattern_type=constant.URL_WALK,
        pattern='.*'
    )
    WebsiteSelector.objects.create(
        website=instance,
        key_name='title',
        xpath='//head//title'
    )
    WebsiteSelector.objects.create(
        website=instance,
        key_name='body',
        xpath='body'
    )


def signal_register():
    post_save.connect(auto_create_url_pattern, sender=Website)
