"""
Elastic search utils functions
"""

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import mail
from pustakalaya_apps.document.tasks import send_email_to_item_owner
from django.conf import settings
from django.contrib.sites.models import Site


def list_search_from_elastic(request, query_type="match", **kwargs):
    """
    Return a list of matching document when query value matches the field value.

    Usage: list_display(request, "mero katha", "title")

    Search the item in elastic search and return the list of items.
    :param request:
    :param name: name to search
    :param pk: primary key of a search string.
    :return: dict
    """
    # Context holder
    context = {}
    sort_order_type = "asc", "desc"
    sort_by_type = "title.raw", "updated_date"

    if request.method == "GET":
        # Default sort options
        sort_by = request.GET.get("sort_by") or "updated_date"
        sort_order = request.GET.get("sort_order") or "asc"

        if sort_order not in sort_order_type:
            sort_order = "asc"

        if sort_by not in sort_by_type:
            sort_by = "title.keyword"

    # Query to elastic search to grab all the items related to this collection name
    # And sort the result based on the sorting options.
    client = connections.get_connection()
    s = Search().using(client).query(query_type, **kwargs).sort({
        sort_by: {"order": sort_order}
    })

    # print("author name lllll=",author_name)
    # s = Search().using(client).query('term', author_list="First name").sort({
    #      sort_by: {"order": sort_order}
    #  })

    # Pagination configuration before executing a query.
    number_per_page = 15
    paginator = Paginator(s, number_per_page)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    response = page.object_list.execute()

    start_item_count = 0
    # print("pg num= ",page_no)
    if page_no is not None:

        if page_no.isdigit():
            if page_no == 1:
                start_item_count = 1
            elif int(page_no) > 1:
                start_item_count = (int(page_no) - 1) * number_per_page
        else:
            start_item_count = 0

    context["response"] = response
    context["sort_order"] = sort_order
    context["sort_by"] = sort_by
    context["page_obj"] = page
    context["paginator"] = paginator
    context["page_number_count"] = start_item_count

    return context


def list_search_from_elastic_work(request,author_name, query_type="match"):
    """
    Return a list of matching document when query value matches the field value.

    Usage: list_display(request, "mero katha", "title")

    Search the item in elastic search and return the list of items.
    :param request:
    :param name: name to search
    :param pk: primary key of a search string.
    :return: dict
    """
    # Context holder
    context = {}
    sort_order_type = "asc", "desc"
    sort_by_type = "title.raw", "updated_date"

    if request.method == "GET":
        # Default sort options
        sort_by = request.GET.get("sort_by") or "updated_date"
        sort_order = request.GET.get("sort_order") or "asc"

        if sort_order not in sort_order_type:
            sort_order = "asc"

        if sort_by not in sort_by_type:
            sort_by = "title.keyword"

    # Query to elastic search to grab all the items related to this collection name
    # And sort the result based on the sorting options.
    client = connections.get_connection()
    # s = Search().using(client).query(query_type, **kwargs).sort({
    #     sort_by: {"order": sort_order}
    # })
    #print("author name lllll=",author_name)

    s = Search().using(client).query('term', author_list=author_name).sort({
         sort_by: {"order": sort_order}
     })

    # s = Search(using=client, index="pustakalaya") \
    #     .query("match", author_list= "First name") \
    #     .sort({
    #     sort_by: {"order": sort_order}
    #     })


    # s = Search().using(client).query("multi_match",query=author_name,fields=['author_list']).sort({
    #     sort_by: {"order": sort_order}
    # })

    # Pagination configuration before executing a query.
    number_per_page = 15
    paginator = Paginator(s, number_per_page)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    response = page.object_list.execute()

    start_item_count = 0
    # print("pg num= ",page_no)
    if page_no is not None:

        if page_no.isdigit():
            if page_no == 1:
                start_item_count = 1
            elif int(page_no) > 1:
                start_item_count = (int(page_no) - 1) * number_per_page
        else:
            start_item_count = 0

    context["response"] = response
    context["sort_order"] = sort_order
    context["sort_by"] = sort_by
    context["page_obj"] = page
    context["paginator"] = paginator
    context["page_number_count"] = start_item_count

    return context


<<<<<<< HEAD
def send_mail_on_user_submission(item=None):
    """
    Send an email to a user when an item is published to pustakalaya archive. 
    """
    domain_name  = Site.objects.get_current().domain or "http://pustakalaya.org"

    if not item or item.published == "no":
        return 
    else:
        message = """{} has been Published in {}
        click http://{}{} to view the  {} details
         """.format(
             item.title, 
             domain_name,
             domain_name,
             item.get_absolute_url(),
             item.type
         )

        return send_email_to_item_owner.delay(
            "{} has been approved in {}".format(item.title, domain_name),
            message=message, 
            send_to_list=[item.submitted_by.email]
        )

        


=======
def isAuthorAlreadyExist():
    pass
>>>>>>> a4a4e74118b7d5fe847c3e844c1aaa5a6a4ffa5d
