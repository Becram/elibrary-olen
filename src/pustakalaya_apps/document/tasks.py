from __future__ import absolute_import
import os
import logging
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.decorators import task
from celery import (
    shared_task,
    task
)
from django.core.mail import send_mail
from celery.contrib import rdb
from pustakalaya_apps.document.models import DocumentFileUpload

logger = get_task_logger(__name__)


@shared_task(name="pdf to image conversion")
def convert_pdf(file_path, instance_id=None):
    import subprocess
    import os
    """ Convert a PDF into images.
        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png
        The function removes the alpha channel from the image and
        replace it with a white background.
    """

    # Grab the instance from the models
    try:
        file_document = DocumentFileUpload.objects.get(pk=instance_id)
    except DocumentFileUpload.DoesNotExist:
        return

    file_dir, file_name = os.path.split(file_path)

    print("Destinatin Dir:", file_dir)
    print("FileNmae:", file_name)
    print("Conversion aborted since we dont need the conversion, since flibbook option not implemented")
#    print("COnverstion started")
    # Start to convert pdf to jpej
    # success = subprocess.call(['pdftocairo', '-png', file_path, file_dir])
    success = subprocess.call("pdftocairo -png {} {}/".format(file_path, file_dir), shell=True)
    # TODO: Replace with log
    print("conversion finished")

    if success == 0:  #
        total_converted_page = 0
        for image in os.listdir(file_dir):
            if image.startswith('-') and image.endswith('.png'):
                new_image = os.path.join(file_dir, image.lstrip('-0'))
                old_image = os.path.join(file_dir, image)
                subprocess.call(['mv', old_image, new_image])

                total_converted_page += 1
                print(old_image, new_image)

        # Update the document total pages.
        file_document.total_pages = total_converted_page
        # Update the total pages and save this instance.
        file_document.save()


@shared_task(name="send feedback message")
def send_feedback_email_task(title, message, send_to_list=None):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return send_mail(
         title,
         message,
         settings.EMAIL_HOST_USER,
         send_to_list or settings.FEEDBACK_MESSAGE_TO,
         fail_silently=False
         )


@shared_task(name="send email to item owner")
def send_email_to_item_owner(title, message, send_to_list=None):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return send_mail(
         title,
         message,
         settings.EMAIL_HOST_USER,
         send_to_list,
         fail_silently=False
         )

