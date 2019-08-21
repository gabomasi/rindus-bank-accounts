from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User
from .utils import get_audit_user


class UserChangeCustomForm(UserChangeForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    def clean(self):
        if self.instance.created_by and self.instance.created_by != get_audit_user():
            raise ValidationError('You can not edit this user, it was not created by you')


class AdminPasswordChangeCustomForm(AdminPasswordChangeForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    def clean(self):
        if self.user.created_by and self.user.created_by != get_audit_user():
            raise ValidationError('You can not edit this user, it was not created by you')


class UserCreationCustomForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    def save(self, commit=True):
        self.instance.created_by = get_audit_user()
        user = super().save(commit=commit)
        return user


class UserCustomAdmin(UserAdmin):
    form = UserChangeCustomForm
    add_form = UserCreationCustomForm
    change_password_form = AdminPasswordChangeCustomForm


admin.site.register(User, UserCustomAdmin)
