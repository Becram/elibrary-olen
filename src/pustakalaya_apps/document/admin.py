from django.contrib import admin

from .models import (
    Document,
    UnpublishedDocument,
    DocumentSeries,
    DocumentFileUpload,
    DocumentLinkInfo,
    DocumentIdentifier
)


class DocumentFileUploadInline(admin.TabularInline):
    model = DocumentFileUpload
    extra = 1


class DocumentLinkInfoAdminInline(admin.TabularInline):
    model = DocumentLinkInfo
    extra = 1


class DocumentIdentifierAdmin(admin.StackedInline):
    model = DocumentIdentifier
    extra = 1
    max_num = 1

@admin.register(UnpublishedDocument)
class UnpublishedDocumentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return  self.model.objects.filter(published="no")

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        DocumentIdentifierAdmin,
        DocumentLinkInfoAdminInline,
        DocumentFileUploadInline,
    ]

    search_fields = (
        'title',
    )

    fields = (
        "title",
        "abstract",
        "collections",
        "education_levels",
        "languages",
        "featured",
        "published",
        "document_file_type",
        "document_interactivity",
        "document_authors",
        "document_editors",
        "document_illustrators",
        "place_of_publication",
        "publisher",
        "publication_year",
        "year_of_available",
        "keywords",
        "document_series",
        "volume",
        "edition",
        "document_total_page",
        "document_type",
        "additional_note",
        "description",
        "license_type",
        "custom_license",
        "sponsors",
        "thumbnail",
    )

    list_display = ['title', 'published', 'updated_date', 'submitted_by']

    list_filter = ['published', 'title']

    def save_model(self, request, obj, form, change):
        """Override the submitted_by field to admin user
        save_model is only called when the user is logged as an admin user.
        """
        if obj.submitted_by is None:
            obj.submitted_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DocumentSeries)
class DocumentSeriesAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}
