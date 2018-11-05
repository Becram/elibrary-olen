from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from hitcount.models import HitCount
from .serializers import (
    BiographySerializer,
    KeyWordSerializer,
    EducationLevelSerializer,
    LanguageSerializer,
    LicenseTypeSerializer,
    PublisherSerializer,
    SponsorSerializer,
    HitCountSerializer,
)

from pustakalaya_apps.core.models import (
    Biography,
    Keyword,
    Language,
    Publisher,
    EducationLevel,
    Sponsor,
    LicenseType,
)

from pustakalaya_apps.document.models import Document
from pustakalaya_apps.document.api.v1.serializers import DocumentListSerializer

from pustakalaya_apps.audio.models import Audio
from pustakalaya_apps.audio.api.v1.serializers import AudioSerializers

from pustakalaya_apps.video.models import Video
from pustakalaya_apps.video.api.v1.serializers import VideoSerializers


@api_view(['GET'])
def featured_recent_popular_list(request, format=None):
    """
    Endpoint to get list of featured,recent
    and popular documents
    """

    if request.method == 'GET':
        featured_documents = Document.featured_objects.all()
        featured_documents_serializer = DocumentListSerializer(featured_documents, many=True)
        recent_documents = Document.objects.filter(published="yes").order_by("-created_date")[:6]
        recent_documents_serializer = DocumentListSerializer(recent_documents, many=True)
        popular_documents = HitCount.objects.filter(hit_count_generic_relation__published="yes")[:6]
        popular_documents_serializer = HitCountSerializer(popular_documents, many=True)
        return Response(
            [{'featured_documents': featured_documents_serializer.data,
              'recent_documents': recent_documents_serializer.data,
              'popular_documents': popular_documents_serializer.data}],
            status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def items_list_by_collection(request, pk):
    """
    Endpoint to get list of audios, videos
    and documents based on collection
    """
    try:
        documents = Document.objects.filter(published="yes", collections=pk).order_by("-created_date")
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        documents_serializer = DocumentListSerializer(documents, many=True)

        # To be implemented while implementing audios and videos API
        # audios = Audio.objects.filter(published="yes", collections=pk).order_by("-created_date")
        # audios_serializer = AudioSerializers(audios, many=True)
        # videos = Video.objects.filter(published="yes", collections=pk).order_by("-created_date")
        # videos_serializer = VideoSerializers(videos, many=True)
        return Response(
            [{'documents': documents_serializer.data,
              'audios': [],
              'videos': []}],
            status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class BiographyViewSet(viewsets.ModelViewSet):
    """
    Endpoint to CRUD Authors
    """
    queryset = Biography.objects.all()
    serializer_class = BiographySerializer


biography_list = BiographyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

biography_detail = BiographyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class KeywordViewSet(viewsets.ModelViewSet):
    """
     Keyword endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for keyword
    """
    queryset = Keyword.objects.all()
    serializer_class = KeyWordSerializer


keyword_list = KeywordViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

keyword_detail = KeywordViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class LanguageViewSet(viewsets.ModelViewSet):
    """
    Language endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Language links
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


language_list = LanguageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

language_detail = LanguageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class PublisherViewSet(viewsets.ModelViewSet):
    """
    Publisher endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for publisher links
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


publisher_list = PublisherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

publisher_detail = PublisherViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class EducationLevelViewSet(viewsets.ModelViewSet):
    """
     Education Level endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Education Level 
    """
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


educationlevel_list = EducationLevelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

educationlevel_detail = EducationLevelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class SponsorViewSet(viewsets.ModelViewSet):
    """
     sponsors endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for sponsors
    """
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


sponsor_list = SponsorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

sponsor_detail = SponsorViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class LicenseTypeViewSet(viewsets.ModelViewSet):
    """
     Licese type endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for LicenseType
    """
    queryset = LicenseType.objects.all()
    serializer_class = LicenseTypeSerializer


licensetype_list = LicenseTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

licensetype_detail = LicenseTypeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})



