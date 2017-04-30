from rest_framework import serializers

from so.models import (
    Website,
    WebsiteAllowedDomain,
    WebsiteUrlPattern,
    WebsiteSelector,
    SpiderTask,
)


class WebsiteSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Website
        fields = ('id', 'title', 'sleep_seconds', 'schedule_type',
                  'expire_seconds')


class WebsiteAllowedDomainSerializer(serializers.ModelSerializer):
    website_id = serializers.PrimaryKeyRelatedField(
        source='website',
        queryset=Website.objects.all()
    )

    class Meta:
        model = WebsiteAllowedDomain
        fields = ('id', 'website_id', 'domain')


class WebsiteUrlPatternSerializer(serializers.ModelSerializer):
    website_id = serializers.PrimaryKeyRelatedField(
        source='website',
        queryset=Website.objects.all()
    )

    class Meta:
        model = WebsiteUrlPattern
        fields = ('id', 'website_id', 'pattern_type', 'pattern')


class WebsiteSelectorSerializer(serializers.ModelSerializer):
    website_id = serializers.PrimaryKeyRelatedField(
        source='website',
        queryset=Website.objects.all()
    )

    class Meta:
        model = WebsiteSelector
        fields = ('id', 'website_id', 'key_name', 'xpath')


class SpiderTaskSerializer(serializers.ModelSerializer):
    website = serializers.SerializerMethodField()

    class Meta:
        model = SpiderTask
        fields = ('id', 'website', 'status', 'spider', 'created_at',
                  'updated_at')

    def get_website(self, instance):
        website = Website.objects.get(pk=instance.website_id)
        return website.title
