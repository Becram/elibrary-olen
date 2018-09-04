from django.contrib import admin
from .models import Review
from  django.utils.html import format_html
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'post', 'created', 'user_email')

    search_fields = ('user', 'post', 'published')
    list_filter = ('published',)
    # def get_queryset(self, request):
    #     return self.model.objects.filter(published="False")

    def user_email(self, obj):
        return format_html("{email}", email=obj.user.email)


admin.site.register(Review, ReviewAdmin)
