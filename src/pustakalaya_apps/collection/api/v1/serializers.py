from rest_framework import serializers
from pustakalaya_apps.collection.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    count = serializers.CharField(source='get_item_count')

    class Meta:
        model = Collection 
        fields = '__all__'

