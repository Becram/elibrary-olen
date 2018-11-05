from rest_framework import serializers
from hitcount.models import HitCount
from pustakalaya_apps.core.models import (
    Biography,
    Keyword,
    Language,
    Publisher,
    EducationLevel,
    Sponsor,
    LicenseType,
)


# Core serializers. 
class BiographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Biography 
        fields = '__all__'


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword 
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language 
        fields = '__all__'


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel 
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher 
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor 
        fields = '__all__'


class LicenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseType 
        fields = '__all__'


# HitCount Serializer.
class HitCountSerializer(serializers.ModelSerializer):
    """
    Class to serialize HitCount data types.
    """
    id = serializers.UUIDField(source='object_pk')
    title = serializers.CharField(source='content_object.title')
    abstract = serializers.CharField(source='content_object.abstract')
    type = serializers.CharField(source='content_object.type')
    document_type = serializers.CharField(source='content_object.document_type')
    document_total_page = serializers.CharField(source='content_object.document_total_page')
    thumbnail = serializers.ImageField(source='content_object.thumbnail')

    class Meta:
        model = HitCount
        exclude = ('object_pk', 'modified', 'content_type', )

