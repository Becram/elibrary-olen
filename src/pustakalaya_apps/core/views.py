from itertools import chain
from pustakalaya_apps.document.models import Document
from pustakalaya_apps.audio.models import AudioFileUpload
from pustakalaya_apps.video.models import VideoFileUpload
from pustakalaya_apps.core.models import Biography
from pustakalaya_apps.audio.models import Audio
from pustakalaya_apps.video.models import Video
from django.shortcuts import (
    render,
)

import logging

import datetime
from django.conf import settings


def home(request):
    """view that serve homepage"""

    #BIKRAM log testing
    logger = logging.getLogger('app.logger')

    try:
        # Based on hit count so, need to capture Field error exception
        featured_books = Document.featured_objects.all() # Return top 4 views item.
        no_of_featured= len(featured_books)
        logger.info('Number of featured Book %s' % no_of_featured)

    except Exception as e:  # Catch all error don't know what kind exist.
        pass

    featured_audio = Audio.featured_objects.all()  # Provide only top 2 items

    featured_video = Video.featured_objects.all()  # Provide only top 2 items

    if not featured_books:
        featured_books = Document.objects.filter(featured="yes", published="yes").order_by('-updated_date')[:3]

    if not featured_audio:
        featured_audio = Audio.objects.filter(featured="yes", published="yes").order_by('-updated_date')[:3]

    if not featured_video:
        featured_video = Video.objects.filter(featured="yes", published="yes").order_by('-updated_date')[:2]

    items = list(chain(featured_books, featured_audio,  featured_video))

    # Sorting data according to updated date among audio video document
    item_sorted = sorted(items, key=lambda x: x.updated_date, reverse=True)

    # Get the total audio, videos and author count
    total_document = Document.objects.filter(published="yes").count()
    total_audio = AudioFileUpload.objects.count()
    total_video = VideoFileUpload.objects.count()
    total_authors = Biography.objects.count()

    context = {}
    context['total_document'] = total_document
    context['total_audio'] = total_audio
    context['total_video'] = total_video
    context['total_authors'] = total_authors
    context["featured_books"] = list(item_sorted)
    return render(request, "index.html", context)
