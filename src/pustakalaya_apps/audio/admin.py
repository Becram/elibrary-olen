from django.contrib import admin
from .models import (
    AudioFileUpload,
    Audio,
    AudioGenre,
    AudioSeries,
    AudioLinkInfo,
    AudioType
)


class AudioFileUploadInline(admin.StackedInline):
    model = AudioFileUpload
    extra = 1


class AudioLinkInfoAdminInline(admin.StackedInline):
    model = AudioLinkInfo
    extra = 1


@admin.register(Audio)
class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        AudioLinkInfoAdminInline,
        AudioFileUploadInline,
    ]

    list_per_page = 10

    fields = (
        "title",
        "abstract",
        "collections",
        "education_levels",
        "languages",
        "place_of_publication",
        "publisher",
        "year_of_available",
        "audio_types",
        "audio_running_time",
        "audio_read_by",
        "published",
        "audio_genre",
        "keywords",
        "audio_series",
        "volume",
        "edition",
        "additional_note",
        "description",
        "license_type",
        "custom_license",
        "publication_year",
        "sponsors",
        "thumbnail"
    )


@admin.register(AudioGenre)
class AudioGenreAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(AudioSeries)
class AudioSeriesAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(AudioType)
class AudioTypeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
