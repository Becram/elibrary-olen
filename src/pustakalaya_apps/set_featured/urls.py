from django.conf.urls import url
from . import views

# Application level namespace.
app_name = "set_featured"

urlpatterns = [
    # /review_system/
    url(r'^$', views.set_featured_view, name="featured_view"),
    url(r'^featured_unset/$', views.unset_featured_view, name="featured_remove"),

]
