from django.db import migrations
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.management import create_permissions
from bankaccounts import constants


def add_permissions(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    admin_group = Group.objects.get_or_create(
        name=constants.BANK_ACCOUNT_ADM_GROUP)[0]
    bank_permissions = Permission.objects.filter(content_type__app_label='bankaccounts')
    admin_group.permissions.set(bank_permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('bankaccounts', '0002_bankaccount'),
    ]

    operations = [
        migrations.RunPython(add_permissions),
    ]
