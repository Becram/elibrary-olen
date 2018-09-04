from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from pustakalaya_apps.audio.models import Audio
from .forms import AudioFileUploadForm,AudioForm, AudioFileUploadFormSet,AudioReadBy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class AddAudioView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Audio
    form_class = AudioForm
    template_name = "dashboard/audio/audio_add.html/"
    success_url = "/dashboard/"


    def get_context_data(self, **kwargs):
        context = super(AddAudioView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["audio_form"] = AudioForm(self.request.POST)
            # context["audio_read_by"] = AudioReadBy(self.request.POST)
            context['audio_file_upload_form'] = AudioFileUploadFormSet(self.request.POST, self.request.FILES,
                                                                       instance=self.object)

        else:
            context["audio_form"] = AudioForm()
            # context["audio_read_by"] = AudioReadBy()
            context['audio_file_upload_form'] = AudioFileUploadFormSet()

        return context


    def form_valid(self, form):
        context = self.get_context_data()
        # form upload inlines
        inlines = context["audio_file_upload_form"]
        # form = context["form"]
        status = form.is_valid()
        statusset = inlines.is_valid()

        if form.is_valid() and inlines.is_valid():
            # Save the object. and its children.
            self.object = form.save(commit=False)
            # Make published to no, as admin will review and set to yes.
            self.object.published = "no"
            self.object.submitted_by = self.request.user
            self.object.save()
            form.save_m2m()  # Save other m2m fields.
            # Here instance is Document.
            inlines.instance = self.object
            inlines.save()



            # Clear all other message and add message
            storage = messages.get_messages(self.request)
            storage.used = True

            messages.add_message(
               self.request,
                messages.SUCCESS,
                'Audio added successfully, we will notify you after reviewing it'
                )
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

            # Handle the form in case all the invalid form.

    def form_invalid(self, form):
        print("Form is valid or invalid")
        return self.render_to_response(self.get_context_data(form=form))


class UpdateAudioView(LoginRequiredMixin, UpdateView):
    model = Audio
    fields = [
                'title',
                # 'collections',
                # 'education_levels',
                'description',
                # 'languages',
                # 'publisher',
                # 'audio_types',
                # 'audio_read_by',
                # 'audio_genre',
                # 'keywords',
                # 'audio_series',
                # 'license_type'
    ]

    template_name = "dashboard/audio/audio_edit.html/"
    success_url = '/dashboard/submission/list/'

    def clean(self, UpdateAudioView):
        cleaned_data = super(UpdateAudioView, self).clean()
        title = cleaned_data.get('title')
        # collections = cleaned_data.get('collections')
        description = cleaned_data.get('description')
        # education_levels = cleaned_data.get('education_levels')
        # languages = cleaned_data.get('languages')
        # audio_types = cleaned_data.get('audio_types')
        # publisher = cleaned_data.get('publisher')
        # audio_types = cleaned_data.get('audio_types')
        # audio_read_by = cleaned_data.get('audio_read_by')
        # audio_genre = cleaned_data.get('audio_genre')
        # keywords = cleaned_data.get('keywords')
        # audio_series = cleaned_data.get('audio_series')
        # license_type = cleaned_data.get('license_type')

        # if not title and not collections and not education_levels and not languages and not \
        #     audio_types and not publisher and not audio_types and not keywords and not audio_read_by \
        #     and not audio_genre and not audio_series and not license_type:
        #     raise cleaned_data.ValidationError('You have to write something!')
        if not title:
            raise cleaned_data.ValidationError('You have to write something!')


class DeleteAudioView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Audio
    fields = [
                'title',
                'collections',
                'education_levels',
                'languages',
                'publisher',
                'audio_types',
                'audio_read_by',
                'audio_genre',
                'keywords',
                'audio_series',
                'license_type'
    ]

    template_name = "dashboard/audio/audio_delete.html/"
    success_url = '/dashboard/submission/list/'
    success_message = "was deleted successfully"


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteAudioView, self).delete(request, *args, **kwargs)

