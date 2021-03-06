from __future__ import print_function
import os
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save, pre_delete, m2m_changed
from .models import Document, DocumentFileUpload
from .tasks import convert_pdf
from pustakalaya_apps.core.utils import send_mail_on_user_submission
from django.contrib.auth.models import  User


@receiver(m2m_changed, sender=Document.keywords.through)
@receiver(m2m_changed, sender=Document.document_authors.through)
@receiver(m2m_changed, sender=Document.education_levels.through)
@receiver(m2m_changed, sender=Document.document_illustrators.through)
@receiver(m2m_changed, sender=Document.document_editors.through)
@receiver(m2m_changed, sender=Document.collections.through)
@receiver(m2m_changed, sender=Document)
@receiver(post_save, sender=Document)
@transaction.atomic
def index_or_update_document(sender, instance, **kwargs):
    # send an email to user when the document is published.

    # By pass for unpublished items
    if instance.published == "no":
        return

    if instance.published == "yes":
        # added to restrict the if user is super user
        # if not sender is User.is_superuser:
        print("whois sender=",sender,"is suerp =",User.is_superuser)
        send_mail_on_user_submission(item=instance)


    if instance.license is not None:
        if instance.license:
            instance.license_type = instance.license.license

    # Save or update index
    instance.index()


@receiver(pre_delete, sender=Document)
@transaction.atomic
def delete_document(sender, instance, **kwargs):

     # By pass for unpublished items
    if instance.published == "no":
        return

    # Delete an index first before instance in db.
    instance.delete_index()


@receiver(post_save, sender=DocumentFileUpload)
def pdfto_image(sender, instance, **kwargs):
    """
    Convert pdf to images
    """
    # dissable this feature no use now
    return

    # grab the file path
    file_full_path = instance.upload.path
    file_name = os.path.split(file_full_path)[1]

    if not file_name.lower().endswith('.pdf'):
        return


    if instance.total_pages <= 0: # Document is not converted yet send for conversion.
        convert_pdf.delay(file_full_path, instance_id=instance.pk)
