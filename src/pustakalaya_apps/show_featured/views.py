from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.shortcuts import HttpResponseRedirect
from pustakalaya_apps.document.models import Document
# Create your views here.


def show_all_featured_item(request):

    item_list = Document.objects.filter(featured="yes",published="yes")

    total_count = len(item_list)


    # Pagination configuration before executing a query.
    paginator = Paginator(item_list, 24)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "show_featured/all_featured_item.html", {
        'favourite_documents':page,
        'total_count':total_count,
        'page_obj':page,
        "paginator":paginator
    })


