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




@login_required()
def dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/")


    popular_documents = Document.objects.order_by('-updated_date')[:5]

    # Now lets get the users books first
    item_list = Favourite.objects.filter(user=request.user)

    document_fav_list = []

    for item in item_list:
        # check for document exist or not
        if Document.objects.filter(pk=item.favourite_item_id).exists():
            var = Document.objects.get(pk=item.favourite_item_id)
            document_fav_list.append(var)

    #for pagination we have following code
    paginator = Paginator(document_fav_list, 10)
    page = request.GET.get('page')
    try:
        fav_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fav_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 7777), deliver last page of results.
        fav_items = paginator.page(paginator.num_pages)

    return render(request, "dashboard/dashboard.html", {
        'popular_documents': popular_documents,
        'favourite_documents':fav_items
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


class ProfileEdit(LoginRequiredMixin, UpdateView):
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

 
        

   
    

   









