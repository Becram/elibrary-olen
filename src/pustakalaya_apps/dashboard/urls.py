from django.conf.urls import url
from . import views
from . import document_views, audio_views, video_views
from . import collection_views

urlpatterns = [

    url(r'^$', views.dashboard, name="dashboard"),
    # show all favourite item
    url(r'^show_all_favourite/$', views.show_all_favourite_item, name="show_all_favourite"),

    # show all favourite item
    url(r'^show_all_rated/$', views.show_all_rated_item, name="show_all_rated"),

    # show all reviewed item
    url(r'^show_all_reviewed/$', views.show_all_reviewed_item, name="show_all_reviewed"),


    # url(r'^profile/$', views.profile, name="profile"),
    # /dashboard/profile/edit/
    url(r'^profile/edit/(?P<pk>\d+)/$', views.ProfileEdit.as_view(), name="profile_edit"),

    # dashboard/add/document/
    url(r'^document/add/$', document_views.AddDocumentView.as_view(), name="document_add"),
    # /dashboard/document/update/
    url(r'^document/update/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/', document_views.UpdateDocumentView.as_view(), name="document_update"),
    # /dashboard/document/delete/
    url(r'^document/delete/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/', document_views.DeleteDocumentView.as_view(), name="document_delete"),

    # user submitted items
    url(r'^submission/list/$', document_views.user_submission, name="user_submission"),

    # /dashboard/audio/add/
    url(r'^audio/add/$', audio_views.AddAudioView.as_view(), name="audio_add"),
    # /dashboard/audio/update/
    url(r'^audio/update/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/', audio_views.UpdateAudioView.as_view(), name="audio_update"),
    url(r'^audio/delete/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/',audio_views.DeleteAudioView.as_view(), name="audio_delete"),

    # /dashboard/video/add/
    url(r'^video/add/$', video_views.AddVideoView.as_view(), name="video_add"),
    # /dashboard/video/update/
    url(r'^video/update/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/', video_views.UpdateVideoView.as_view(), name="video_update"),
    url(r'^video/delete/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/',video_views.DeleteVideoView.as_view(), name="video_delete"),

    url(r'^collection/add/$', collection_views.AddCollection.as_view(), name="collection_add"),
    #/dashboard/collections/
    url(r'^collection/add/$', collection_views.AddCollection.as_view(), name="collection_list"),
]
