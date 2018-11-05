from rest_framework import serializers
from pustakalaya_apps.document.models import (
    Document, 
    DocumentFileUpload,
    DocumentLinkInfo,
    DocumentSeries,
    DocumentIdentifier
) 
from pustakalaya_apps.core.api.v1.serializers import (
    BiographySerializer,
    KeyWordSerializer,
    LanguageSerializer,
    LicenseTypeSerializer,
    PublisherSerializer,
)
from pustakalaya_apps.collection.api.v1.serializers import CollectionSerializer


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'abstract', 'type', 'document_type', 'document_total_page', 'thumbnail', )


class DocumentLinkInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLinkInfo
        fields = '__all__'


class DocumentFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentFileUpload
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    """
    Class to serialize document data types. 
    """

    documentfileupload_set = DocumentFileSerializer(many=True)
    documentlinkinfo_set = DocumentLinkInfoSerializer(many=True)
    collections = CollectionSerializer(many=True)
    languages = LanguageSerializer(many=True)
    document_authors = BiographySerializer(many=True)
    document_editors = BiographySerializer(many=True)
    document_translator = BiographySerializer(many=True)
    publisher = PublisherSerializer(many=True)
    keywords = KeyWordSerializer(many=True)

    class Meta:
        model = Document
        fields = '__all__'


class DocumentSeriesSerializer(serializers.ModelSerializer):
    """
    Class to serialize document Series data types. 
    """
    class Meta:
        model = DocumentSeries
        fields = '__all__'


class DocumentIdentifierSerializer(serializers.ModelSerializer):
    """
    Class to serialize DocumentIdentifier data types. 
    """
    class Meta:
        model = DocumentIdentifier
        fields = '__all__'  