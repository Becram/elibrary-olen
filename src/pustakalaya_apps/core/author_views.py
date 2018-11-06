import string
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from collections import defaultdict
from django.views.generic.detail import DetailView
from .models import Biography
from django.shortcuts import (
    render,
)
from pustakalaya_apps.document.models import Document
import re

# English letters
letters = [ letter for letter in string.ascii_lowercase]
# Nepali letters
nepali_letters = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऋ', 'ए', 'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ','ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'स','ष', 'ह']
# All letters
all_letters = letters + nepali_letters


def home(request):
    return render(request, "index.html", {})


class AuthorDetail(DetailView):
    model = Biography

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        books = Document.objects.filter(Q(document_authors=self.object.pk) |
                                        Q(document_editors=self.object.pk) |
                                        Q(document_illustrators=self.object.pk)).distinct()
        print('books......', books)
        context["books"] = books
        print("authors in = ", self.object.authors_name_in_other_language.all())
        # author_other_books = []

        authors_name_in_other_language = self.object.authors_name_in_other_language.all()

        other_books = Document.objects.filter(
            Q(document_authors__in=authors_name_in_other_language) |
            Q(document_editors__in=authors_name_in_other_language) |
            Q(document_illustrators__in=authors_name_in_other_language)).distinct()

        # for author in self.object.authors_name_in_other_language.all():
        #     author_other_books.append(Document.objects.filter(Q(document_authors=author.pk) |
        #                                                       Q(document_editors=author.pk) |
        #                                                       Q(document_illustrators=author.pk)).distinct())
        # context["author_other_books"] = author_other_books
        # print('author other books.......', author_other_books)

        all_books = Document.objects.filter(Q(id__in=books) | Q(id__in=other_books), published="yes")
        print('all books.....', all_books)
        paginator = Paginator(all_books, 18)
        page_no = request.GET.get('page')
        try:
            page = paginator.page(page_no)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        response = page.object_list
        print('response....' , response)

        context["all_books"] = response
        context["page_obj"] = page
        context["paginator"] = paginator


        return self.render_to_response(context)

    template_name = "core/author_detail_new.html"


def author_list(request):
    # dict to hold the list of authors
    author_dict = defaultdict(list)

    # O(n^2) BAD: TODO:
    # Solution1: Save in cache and return the cached value
    # Solution 2: Change the design and use pagination
    # Solution 3: Use ajax in frontend, detect scroll and query the data based on scrolling.
    # Previous design was based on pagination which is in author_list_old.html

    #Filter for show all
    letter_exist = False;

    if request.method == "GET":

        # Author list, BAD, current design don't support pagination, we need to load in single page.
        author_list = Biography.objects.all()

        # For current design. BAD O(N^2)
        for letter in all_letters:
            for name in author_list:
                if name.getname.lower().startswith(letter):
                    author_dict[letter].append(name)


        # query_letter = request.GET.get('letter',None)

        # if not query_letter:
        #     author_list = Biography.objects.all()
        #     author_list2 =""
        # else:
        #     #author_list = Biography.objects.filter(name__startswith=query_letter or query_letter.upper())
        #     # check if the letters are in alphabets
        #     if re.match(r'^[a-zA-Z]+\Z', query_letter):
        #         author_list = Biography.objects.filter(name__startswith=query_letter.lower())
        #         author_list2 = Biography.objects.filter(name__startswith=query_letter.upper())

        #     else:
        #         author_list = Biography.objects.filter(name__startswith=query_letter)
        #         author_list2=""

        #     letter_exist = True


        # new_list = []
        # for item in author_list:
        #     if item.name:
        #         new_list.append(item)

        # for item in author_list2:
        #     if item.name:
        #         new_list.append(item)

        # # Paginate the results
        # number_per_page = 15
        # # Get the page no.

        # page_no = request.GET.get('page')

        # paginator = Paginator(new_list, number_per_page)
        # try:
        #     authors = paginator.page(page_no)
        # except PageNotAnInteger:
        #     authors = paginator.page(1)
        # except EmptyPage:
        #     authors = paginator.page(paginator.num_pages)

        # start_item_count = 0
        # # print("pg num= ",page_no)
        # if page_no is not None:

        #     if page_no.isdigit():
        #         if page_no == 1:
        #             start_item_count = 1
        #         elif int(page_no) > 1:
        #             start_item_count = (int(page_no) - 1) * number_per_page
        #     else:
        #         start_item_count = 0

    return render(request, "core/author_list.html", {
        "letters": letters,
        # "authors": authors,
        "nepali_letters": nepali_letters,
        # "page_number_count" : start_item_count,
        # "letter_exist":letter_exist,
        # "letter":query_letter,
        "author_dict": author_dict
    })

def author_books(request, author_name):
    from pustakalaya_apps.core.utils import list_search_from_elastic
    from pustakalaya_apps.core.utils import  list_search_from_elastic_work
    """
    Query all the books by this author from ES.
    :param request:
    :param author_name:
    :return:
    """
    #print("author name = ",author_name)
    # author_name = " ".join(author_name.split("-"))
    author_name = " ".join(author_name.split("_"))
    #print(author_name)
    # TODO: explicitly define the index name
    search_field = "author_list"
    search_value = author_name
    kwargs = {
        search_field: search_value
    }

    # Query to elastic search in keywords field having the value of search_value
    # Return response object.

    #context = list_search_from_elastic(request, **kwargs)
    context = list_search_from_elastic_work(request,author_name)

    context["keyword"] = context
    context["author"] = author_name
    # Reuse the keyword template
    return render(request, "core/author_books.html", context)
