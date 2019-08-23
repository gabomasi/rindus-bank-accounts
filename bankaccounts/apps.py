from django.apps import AppConfig


class BankaccountsConfig(AppConfig):
    name = 'bankaccounts'

    def ready(self):
        from bankaccounts.signals import update_user_groups
