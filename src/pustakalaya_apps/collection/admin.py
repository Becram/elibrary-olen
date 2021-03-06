from django.contrib import admin
from .models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["collection_name", "community_name"]
    search_fields = (
        'collection_name',
    )
    list_filter = [ 'community_name']
