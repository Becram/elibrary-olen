from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from pustakalaya_apps.audio.models import Audio
from rest_framework.views import APIView
from .serializers import AudioSerializers


class AudioList(APIView):
    """
    List all audio, or create a new audio.
    """
    def get(self, request, format=None):
        audios = Audio.objects.all()
        serializer = AudioSerializers(audios, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):   
        serializer = AudioSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AudioDetail(APIView):
    """
    Retrieve, update or delete a Audio instance.
    """
    def get_object(self, pk):
        try:
            return Audio.objects.get(pk=pk)
        except Audio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        audio = self.get_object(pk)
        serializer = AudioSerializers(audio)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        audio = self.get_object(pk)
        serializer = AudioSerializers(audio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        audio = self.get_object(pk)
        audio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)