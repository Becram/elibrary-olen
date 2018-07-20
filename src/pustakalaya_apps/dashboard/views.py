from itertools import chain
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pustakalaya_apps.pustakalaya_account.models import UserProfile
from django.contrib.auth.decorators import login_required
from pustakalaya_apps.document.models import Document
from pustakalaya_apps.favourite_collection.models import Favourite
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib.messages.views import SuccessMessageMixin
from django.template import RequestContext
from pustakalaya_apps.document.models import Document
from pustakalaya_apps.audio.models import Audio
from pustakalaya_apps.video.models import Video


from star_ratings.models import UserRating
from pustakalaya_apps.review_system.models import Review

@login_required()
def dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/")

    # Featured item
    featured_items = chain(
        Document.featured_objects.all(),
        Audio.featured_objects.all(),
        Video.featured_objects.all(),
    )
    # Note:featured_item=16 item max:doc=6 max,aud = 5 max,vid = 5 max,so no memory scarcity

    sorted_featured = sorted(featured_items, key=lambda x: x.updated_date, reverse=True)[:4]

    # Now lets get the users books first
    item_list = Favourite.objects.filter(user=request.user)[:4]
    document_fav_list = []
    for item in item_list:
        # check if document exist or not
        # Currently we only have fav for doc but for audio and video will be added soon
        if item.favourite_item_type == "document":

            if Document.objects.filter(pk=item.favourite_item_id).exists():
                var = Document.objects.get(pk=item.favourite_item_id)
                document_fav_list.append(var)

        elif item.favourite_item_type == "video":
            if Video.objects.filter(pk=item.favourite_item_id).exists():
                var = Video.objects.get(pk=item.favourite_item_id)
                document_fav_list.append(var)
        else:
            # audio
            if Audio.objects.filter(pk=item.favourite_item_id).exists():
                var = Audio.objects.get(pk=item.favourite_item_id)
                document_fav_list.append(var)


    # item user has rated, for rating done by user
    rating_obj = UserRating.objects.filter(user_id=request.user.pk)[:4]
    list_rating = []

    for item in rating_obj:
        # item.rating.object_id, item.rating.content_type,item.rating.content_object,
        # item.rating.average, item.rating.total,item.rating.count,item.score
        list_rating.append(item.rating.content_object)

    # Review item
    review_data = Review.objects.filter(user=request.user)[:4]  # pull only 4 data first

    # featured item list
    combined_review_list = []
    for item in review_data:

        if item.content_type == "document":
            if Document.objects.filter(pk=item.content_id).exists():
                combined_review_list.append(Document.objects.get(pk=item.content_id))

        elif item.content_type == "video":
            if Video.objects.filter(pk=item.content_id).exists():
                combined_review_list.append(Video.objects.get(pk=item.content_id))
        else:
            # audio
            if Audio.objects.filter(pk=item.content_id).exists():
                combined_review_list.append(Audio.objects.get(pk=item.content_id))

    return render(request, "dashboard/dashboard.html", {
        'popular_documents': sorted_featured,
        'favourite_documents': document_fav_list,
        "rated_item": list_rating,
        "reviewed_item":combined_review_list

    })

@login_required()
def profile(request):
    """
    Render the user profile template
    :param request:
    :return:
    """
    return render(request, 'dashboard/profile.html', {
        "user": request.user
    })


def profile_edit(request):
    pass


class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    def get(self, request, *args, **kwargs):

        if str(request.user.pk) != str(kwargs.get('pk')):
            return HttpResponseForbidden("Permission denied")

        return super(ProfileEdit, self).get(request, *args, **kwargs)

    model = User
    fields = (
        'first_name',
        'last_name',
        'email',
    )

    template_name = 'dashboard/profile/profile.html'
    success_url = '/dashboard/'
    success_message = "Profile updated successfully"

@login_required()
def show_all_favourite_item(request):

    if request.user.is_superuser:
        return HttpResponseRedirect("/")


    # item_list = Document.objects.filter(featured="yes",published="yes")
    # Now lets get the users books first
    item_list = Favourite.objects.filter(user=request.user)
    document_fav_list = []
    for item in item_list:
        # check if document exist or not
        if Document.objects.filter(pk=item.favourite_item_id).exists():
            var = Document.objects.get(pk=item.favourite_item_id)
            document_fav_list.append(var)

    total_count = len(item_list)

    # Pagination configuration before executing a query.
    paginator = Paginator(document_fav_list, 12)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "dashboard/show_all_favourite.html", {
        'favourite_documents': page,
        'total_count': total_count,
        'page_obj': page,
        "paginator": paginator
    })


@login_required()
def show_all_rated_item(request):

    if request.user.is_superuser:
        return HttpResponseRedirect("/")

    # item user has rated, for rating done by user
    rating_obj = UserRating.objects.filter(user_id=request.user.pk)
    list_rating = []

    for item in rating_obj:
        # item.rating.object_id, item.rating.content_type,item.rating.content_object,
        # item.rating.average, item.rating.total,item.rating.count,item.score
        list_rating.append(item.rating.content_object)

    total_count = len(list_rating)

    # Pagination configuration before executing a query.
    paginator = Paginator(list_rating, 12)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "dashboard/show_all_rated.html", {
        'rated_item': page,
        'total_count': total_count,
        'page_obj': page,
        "paginator": paginator
    })



@login_required()
def show_all_reviewed_item(request):

    if request.user.is_superuser:
        return HttpResponseRedirect("/")

    # Review item
    review_data = Review.objects.filter(user=request.user)  # pull only 4 data first

    # featured item list
    combined_review_list = []
    for item in review_data:

        if item.content_type == "document":
            doc_item = Document.objects.get(pk=item.content_id)
            # to check if the item is deleted or empty
            if doc_item:
                combined_review_list.append(doc_item)

        elif item.content_type == "video":
            vid_item = Video.objects.get(pk=item.content_id)
            if vid_item:
                combined_review_list.append(vid_item)
        else:
            # audio
            aud_item = Audio.objects.get(pk=item.content_id)
            if aud_item:
                combined_review_list.append(aud_item)

    total_count = len(combined_review_list)

    # Pagination configuration before executing a query.
    paginator = Paginator(combined_review_list, 12)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "dashboard/show_all_reviewed.html", {
        'reviewed_item': page,
        'total_count': total_count,
        'page_obj': page,
        "paginator": paginator
    })









