from itertools import chain
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import HttpResponseRedirect, render
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from pustakalaya_apps.document.models import Document
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.shortcuts import redirect
from pustakalaya_apps.document.models import (
    DocumentFileUpload,
    Document
)

from pustakalaya_apps.audio.models import Audio
from pustakalaya_apps.video.models import Video

from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger

from .forms import (
    DocumentForm,
    DocumentFileUploadFormSet
)


class AddDocumentView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = DocumentForm
    template_name = "dashboard/document/document_add.html/"
    model = Document
    success_url = '/dashboard/'
    success_message = "Profile updated successfully"

    # the inline forms in `inlines`
    def get_context_data(self, **kwargs):
        ctx = super(AddDocumentView, self).get_context_data(**kwargs)
        if self.request.POST:
            ctx['form'] = DocumentForm(self.request.POST)
            ctx['inlines'] = DocumentFileUploadFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            ctx['form'] = DocumentForm()
            ctx['inlines'] = DocumentFileUploadFormSet()
        return ctx

    # 1. Validate Form.
    def form_valid(self, form):
        context = self.get_context_data()
        # form upload inlines
        inlines = context["inlines"]
        # form = context["form"]

        if form.is_valid() and inlines.is_valid():
            # Save the object. and its children.
            self.object = form.save(commit=False)
            # Make published to no, as admin will review and set to yes.
            self.object.published = "no"
            self.object.submitted_by = self.request.user
            self.object.save()
            form.save_m2m() # Save other m2m fields.
            # Here instance is Document.
            inlines.instance = self.object
            inlines.save()

            #Clear all other message and add message
            storage = messages.get_messages(self.request)
            storage.used = True

            messages.add_message(
               self.request,
                messages.SUCCESS,
                 'Document added successfully, we will notify you after reviewing it'
                )
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))



    # Handle the form in case all the invalid form.
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def user_submission(request):
    # Grab all the list in pagination format.
    user = request.user
    # User submitted documents.
    user_documents = Document.objects.filter(submitted_by=user)
    # User submitted audio
    user_audios = Audio.objects.filter(submitted_by=user)
    # User submitted video
    user_videos = Video.objects.filter(submitted_by=user)

    user_submitted_items = list(chain(user_documents, user_audios, user_videos))

    paginator = Paginator(user_submitted_items, 12)

    page_no = request.GET.get('page')
    try:
        page = paginator.page(page_no)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'dashboard/document/user_submitted_books.html', {
        'items': page,
        'page_obj': page,
        "paginator": paginator
    })



class UpdateDocumentView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Document
    fields = [
        'title',
        # 'collections',
        'description',
        # 'document_file_type',
        # 'languages',
        # 'document_interactivity',
        # 'publisher',
        # 'keywords',
        # 'document_series',
        'document_type',
        # 'license_type'
    ]

    template_name = "dashboard/document/document_edit.html/"
    success_url = '/dashboard/submission/list/'
    success_message = "Document updated  successfully"


    def clean(self, UpdateDocument):
        cleaned_data = super(UpdateDocument, self).clean()
        title = cleaned_data.get('title')
        # collections = cleaned_data.get('collections')
        description = cleaned_data.get('description')
        # document_file_type = cleaned_data.get('document_file_type')
        # languages = cleaned_data.get('languages')
        # document_interactivity = cleaned_data.get('document_interactivity')
        # publisher = cleaned_data.get('publisher')
        # keywords = cleaned_data.get('keywords')
        # document_series = cleaned_data.get('document_series')
        document_type = cleaned_data.get('document_type')
        # license_type = cleaned_data.get('license_type')

        # if not title and not collections and not document_file_type and not languages and not document_interactivity and not publisher and not keywords and not document_series and not document_type and not license_type:
        #     raise cleaned_data.ValidationError('You have to write something!')
        if not title:
            raise cleaned_data.ValidationError('You have to write something!')



class DeleteDocumentView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Document
    fields = [
        'title',
        'collections',
        'document_file_type',
        'languages',
        'document_interactivity',
        'publisher',
        'keywords',
        'document_series',
        'document_type',
        'license_type'

    ]

    template_name = "dashboard/document/document_delete.html/"
    success_url = '/dashboard/submission/list/'
    success_message = "Document deleted successfully"


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteDocumentView, self).delete(request, *args, **kwargs)

