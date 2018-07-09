"""
Dashboard forms.
"""
from django import forms
from django.forms import models
from pustakalaya_apps.document.models import Document, DocumentFileUpload
from pustakalaya_apps.audio.models import Audio, AudioFileUpload
from pustakalaya_apps.video.models import Video, VideoFileUpload
from django.forms.models import inlineformset_factory
from django.core.validators import ValidationError
# import magic


class ProfileForm(forms.ModelForm):
    pass
    """
    Model form for profile user
    """
    #
    # class Meta:
    #     model = UserProfile
    #     fields = ["first_name", "last_name", "phone_no", "user.username"]


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'title',
            # 'collections',
            'description',
            'document_file_type',
            'languages',
            # 'document_interactivity',
            'document_type',
            # 'license_type',
            'thumbnail',
        )

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)

        self.fields['thumbnail'].widget.attrs = {
            'class': 'btn btn-block',
            'name': 'myCustomName',
            'placeholder': 'Item thumbnail'
        }
        self.fields['description'].widget.attrs = {
            'height': '380px',
        }
        self.fields['languages'].widget.attrs = {
            'title': 'Multiple selection field: Press Ctrl + click for multiple selection',
        }


class DocumentFileUploadForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(DocumentFileUploadForm, self).clean()

        upload_file = cleaned_data['upload']

        try:
            if upload_file:

                # supported format pdf, msword,mobi,txt ,ott,epub
                supported_types=['application/pdf', 'text/plain', 'application/msword',  'application/vnd.oasis.opendocument.text-template']

                # mimetype_of_file_uploaded = magic.from_buffer(upload_file.file.getvalue(), mime=True)
                mimetype_of_file_uploaded = upload_file.content_type

                val = 0

                for item1 in supported_types:

                    if item1 == mimetype_of_file_uploaded:
                        val = 1
                        break

                if val == 0:
                    raise ValidationError(u'Error! File can only be .pdf,.txt,word and .ott')
        except (RuntimeError, TypeError, NameError, AttributeError) as e:
            print(e)
            raise ValidationError("Error! Something is wrong.File should be .pdf,.txt,word and .ott format ")




    class Meta:
        model = DocumentFileUpload
        fields = (
            'upload',
        )

    def __init__(self, *args, **kwargs):
        super(DocumentFileUploadForm, self).__init__(*args, **kwargs)

        self.fields['upload'].widget.attrs = {
            'class': 'btn btn-block',
            'name': 'myCustomName',
            'placeholder': 'Upload file',
            'required': 'true'
        }


# Document child forms.
DocumentFileUploadFormSet = inlineformset_factory(
    Document,
    DocumentFileUpload,
    form=DocumentFileUploadForm,
    extra=1 ,
    can_delete=False,
    can_order=False,

)



class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = [
            'title',
            # 'collections',
            'description',
            # 'education_levels',
            'languages',
            # 'publisher',
            # 'audio_types',
            'audio_read_by',
            # 'audio_genre',
            # 'keywords',
            # 'audio_series',
            # 'license_type'
        ]

    def __init__(self, *args, **kwargs):
        super(AudioForm, self).__init__(*args, **kwargs)

        self.fields["description"].widget.attrs={
            'height': '380px'
        }
        self.fields['languages'].widget.attrs = {
            'title': 'Multiple selection field: Press Ctrl + click for multiple selection',
        }
        self.fields['audio_read_by'].widget.attrs = {
            'title': 'Multiple selection field: Press Ctrl + click for multiple selection',
        }



class AudioFileUploadForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(AudioFileUploadForm, self).clean()
        upload_file = cleaned_data['upload']

        try:
            if upload_file:

                # supported format pdf, msword,mobi,txt ,ott,epub
                supported_types = ['audio/mp3', 'audio/mpeg', 'audio/ogg','audio/webm','audio/wav','audio/x-wav']

                # mimetype_of_file_uploaded = magic.from_buffer(upload_file.file.getvalue(), mime=True)
                mimetype_of_file_uploaded = upload_file.content_type

                val = 0

                for item1 in supported_types:

                    if item1 == mimetype_of_file_uploaded:
                        val = 1
                        break

                if val == 0:
                    raise ValidationError(u'Error! File can only be .mp3,.webm(audio),.wav or .ogg format')

        except (RuntimeError, TypeError, NameError, AttributeError) as e:
            print(e)
            raise ValidationError("Error! Something is wrong.File should be .mp3,.webm(audio),.wav or .ogg format ")

    class Meta:
        model = AudioFileUpload
        fields = (
            'file_name',
            'upload',
        )

    def __init__(self, *args, **kwargs):
        super(AudioFileUploadForm, self).__init__(*args, **kwargs)

        self.fields['upload'].widget.attrs = {
            'class': 'btn  btn-block',
            'name': 'myCustomName',
            'placeholder': 'Upload file',
            'required': 'true'
        }




# Audio child forms.
AudioFileUploadFormSet = inlineformset_factory(
    Audio,
    AudioFileUpload,
    form=AudioFileUploadForm,
    extra=1,
    can_delete=False,
    can_order=False
)



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            # 'collections',
            'description',
            # 'education_levels',
            'languages',
            # 'publisher',
            'video_director',
            # 'video_genre',
            # 'keywords',
            # 'video_series',
            # 'license_type'
        ]

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget.attrs={
            'height': '380px'
        }
        self.fields['languages'].widget.attrs = {
            'title': 'Multiple selection field: Press Ctrl + click for multiple selection',
        }
        self.fields['video_director'].widget.attrs = {
            'title': 'Multiple selection field: Press Ctrl + click for multiple selection',
        }

class VideoFileUploadForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(VideoFileUploadForm, self).clean()
        #print(cleaned_data)
        upload_file = cleaned_data['upload']
        print("upload file ctype=",upload_file.content_type,"val-")
        try:

            if upload_file:

                # supported format pdf, msword,mobi,txt ,ott,epub
                # mp4, mkv(x-maroska),ogg,.mov(quicktime),.wmv,webm
                supported_types = ['video/mp4', 'video/x-matroska',
                                   'video/ogg','video/quicktime', 'video/x-ms-wmv',
                                   'video/webm']

                # mimetype_of_file_uploaded = magic.from_buffer(upload_file.file.getvalue(), mime=True)

                mimetype_of_file_uploaded = upload_file.content_type

                val = 0

                for item1 in supported_types:

                    if item1 == mimetype_of_file_uploaded:
                        val = 1
                        break

                if val == 0:
                    raise ValidationError(u'Error! File can only be .mp4, .mkv,.ogg,.mov ,.wmv and .webm(video)  format')
        except (RuntimeError, TypeError, NameError,AttributeError) as e:
            print(e)
            raise ValidationError("Error! Something is wrong.File should be .mp4,"
                                  " .mkv,.ogg,.mov ,.wmv and .webm(video) format!")

    class Meta:
        model = VideoFileUpload
        fields = (
            'file_name',
            'upload',
        )

    def __init__(self, *args, **kwargs):
        super(VideoFileUploadForm, self).__init__(*args, **kwargs)

        self.fields['upload'].widget.attrs = {
            'class': 'btn  btn-block',
            'name': 'myCustomName',
            'placeholder': 'Upload file',
            'required': 'true'
        }



# Audio child forms.
VideoFileUploadFormSet = inlineformset_factory(
    Video,
    VideoFileUpload,
    form=VideoFileUploadForm,
    extra=1,
    can_delete=False,
    can_order=False
)


