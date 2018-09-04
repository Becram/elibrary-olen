from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Audio
from pustakalaya_apps.core.utils import send_mail_on_user_submission


@receiver(post_save, sender=Audio.keywords.through)
@receiver(post_save, sender=Audio.collections.through)
@receiver(post_save, sender=Audio.languages.through)
@receiver(post_save, sender=Audio.education_levels.through)
@receiver(post_save, sender=Audio)
@transaction.atomic
def index_or_update_audio(sender, instance, **kwargs):
    """
    Index or update audio instance to es server
    """

     # By pass for unpublished items
    if instance.published == "no":
        return     

    if instance.published == "yes":
        send_mail_on_user_submission(item=instance)

        
    if instance.license is not None:
        if instance.license.license:
            instance.license_type = instance.license.license

    # Update or index audio doc type
    instance.index()

    # send an email to user when the document is published.
    send_mail_on_user_submission(item=instance)
     


@receiver(pre_delete, sender=Audio)
@transaction.atomic
def delete_audio(sender, instance, **kwargs):
    """
    Delete audio instance from es server
    """

      # By pass for unpublished items
    if instance.published == "no":
        return 

        
    # Update or index audio doc type
    # TODO: implement logging
    # TODO: log this event
    instance.delete_index()
