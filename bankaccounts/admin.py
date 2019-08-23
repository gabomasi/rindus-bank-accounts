from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, BankAccount
from .utils import get_audit_user


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
    add_form = UserCreationCustomForm

    def get_queryset(self, request):
        qs = super(UserCustomAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active',)

        return [(None, {'fields': ('username', 'password')}),
                (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (('Permissions'), {'fields': perm_fields}),
                (('Important dates'), {'fields': ('last_login', 'date_joined')})]


class BankAccountAdminForm(forms.ModelForm):

    class Meta:
        model = BankAccount
        fields = '__all__'


class BankAccountAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(BankAccountAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user__created_by=request.user)

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
