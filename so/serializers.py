from rest_framework import serializers

from so.models import (
    Website,
    WebsiteAllowedDomain,
    WebsiteUrlPattern,
    WebsiteSelector,
)


class WebsiteSerialzer(serializers.ModelSerializer):
    allowed_domains = serializers.SerializerMethodField()
    url_patterns = serializers.SerializerMethodField()
    selectors = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = ('title', 'sleep_seconds', 'schedule_type',
                  'expire_seconds', 'allowed_domains',
                  'url_patterns', 'selectors')

    def get_allowed_domains(self, instance):
        allowed_domains = WebsiteAllowedDomain.objects.filter(website=instance)
        return WebsiteAllowedDomainSerializer(allowed_domains, many=True).data

    def get_url_patterns(self, instance):
        url_patterns = WebsiteUrlPattern.objects.filter(website=instance)
        return WebsiteUrlPatternSerializer(url_patterns, many=True).data

    def get_selectors(self, instance):
        selectors = WebsiteSelector.objects.filter(website=instance)
        return WebsiteSelectorSerializer(selectors, many=True).data


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
