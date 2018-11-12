from django.contrib import admin
from django.utils.html import format_html
from .models import Review
from pustakalaya_apps.document.models import Document
from pustakalaya_apps.audio.models import Audio
from pustakalaya_apps.video.models import Video


class ReviewAdmin(admin.ModelAdmin):

    list_display = ('title', 'reviewed_item', 'user', 'post', 'created', 'user_email')
    search_fields = ('user__first_name', 'user__email', 'post')
    list_filter = ('published', 'content_type')
    list_per_page = 25

    # def get_queryset(self, request):
    #     return self.model.objects.filter(published="False")

    def user_email(self, obj):
        return format_html("{email}", email=obj.user.email)

    def reviewed_item(self, obj):
        if obj.content_type == 'document':
            item = Document.objects.get(pk=obj.content_id)
        elif obj.content_type == 'audio':
            item = Audio.objects.get(pk=obj.content_id)
        elif obj.content_type == 'video':
            item = Video.objects.get(pk=obj.content_id)
        else:
            item = None

        if item:
            return format_html('<a href="%s">%s</a>' %(item.get_absolute_url(), item.title))
        else:
            return None


admin.site.register(Review, ReviewAdmin)
