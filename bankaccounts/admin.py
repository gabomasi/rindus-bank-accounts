from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms
from .models import User, BankAccount
from .utils import get_audit_user


class UserChangeCustomForm(UserChangeForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    def clean(self):
        if (not self.instance.created_by) or (self.instance.created_by and self.instance.created_by != get_audit_user()):
            raise ValidationError('You can not edit this user, it was not created by you')


class AdminPasswordChangeCustomForm(AdminPasswordChangeForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    def clean(self):
        if (not self.instance.created_by) or (self.instance.created_by and self.instance.created_by != get_audit_user()):
            raise ValidationError('You can not edit this user, it was not created by you')


class UserCreationCustomForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    def save(self, commit=True):
        self.instance.created_by = get_audit_user()
        self.instance.is_staff = True
        user = super().save(commit=commit)
        return user


class UserCustomAdmin(UserAdmin):
    form = UserChangeCustomForm
    add_form = UserCreationCustomForm
    change_password_form = AdminPasswordChangeCustomForm


class BankAccountAdminForm(forms.ModelForm):

    class Meta:
        model = BankAccount
        fields = '__all__'


class BankAccountAdmin(admin.ModelAdmin):
    search_fields = ['iban']
    list_display = ['iban', 'user']
    form = BankAccountAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(created_by=get_audit_user())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(User, UserCustomAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.login_template = "bankaccounts/login.template.html"
