from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from bankaccounts import constants


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_groups(sender, instance=None, created=False, **kwargs):
    if created:
        instance.groups.add(Group.objects.get_or_create(
            name=constants.BANK_ACCOUNT_ADM_GROUP)[0])
        instance.is_staff = True
        instance.save()
