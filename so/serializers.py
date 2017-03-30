from rest_framework import serializers

from so.models import (
    Website,
    WebsiteAllowedDomain,
    WebsiteUrlPattern,
    WebsiteSelector,
)


class WebsiteSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Website


class WebsiteAllowedDomainSerializer(serializers.ModelSerializer):
    website_id = serializers.PrimaryKeyRelatedField(
        srouce='website',
        queryset=Website.objects.all()
    )

    class Meta:
        model = WebsiteAllowedDomain
        fields = ('id', 'website_id', 'domain')


class WebsiteUrlPatternSerializer(serializers.ModelSerializer):
    website_id = serializers.PrimaryKeyRelatedField(
        srouce='website',
        queryset=Website.objects.all()
    )

    class Meta:
        model = WebsiteUrlPatternSerializer
        fields = ('id', 'website_id', 'pattern_type', 'pattern')


class WebsiteSelector(serializers.ModelSerializer):
    website_id = serializers.PrimaryKeyRelatedField(
        srouce='website',
        queryset=Website.objects.all()
    )

    class Meta:
        model = WebsiteSelector
        fields = ('id', 'website_id', 'key_name', 'xpath')
