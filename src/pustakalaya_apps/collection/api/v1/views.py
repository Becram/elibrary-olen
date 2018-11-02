from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CollectionSerializer
from pustakalaya_apps.collection.models import Collection
from rest_framework import permissions
from rest_framework import renderers


@api_view(['GET'])
def collection_by_category(request, community_name):
    """
    Endpoint to get list of collections based on categories
    """

    if request.method == 'GET':
        community_name = community_name.replace('-', ' ')
        collection_list_by_category = Collection.objects.filter(community_name=community_name)
        collection_list_serializer = CollectionSerializer(collection_list_by_category, many=True)
        return Response(collection_list_serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CollectionViewSet(viewsets.ModelViewSet):
    """
     Collection endpoint to  `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Collection model
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


collection_list = CollectionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
collection_detail = CollectionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})



