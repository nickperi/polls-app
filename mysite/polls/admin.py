from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

# Register your models here.
from .models import Question, Choice, Voter

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {"fields": ["question_text"]}), 
    ("Date Information", {"fields": ["pub_date"], "classes": ["collapse"],}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


class VoterRegistrationForm(UserCreationForm):
    class Meta:
        model = Voter
        fields = ["first_name", "last_name", "username", "email", "date_of_birth", "password1", "password2"]
    

class VoterChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Voter
        fields = ["email", "password", "date_of_birth", "is_active", "is_admin"]


class VoterAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = VoterChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "date_of_birth", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["first_name", "last_name", "email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["username", "email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(Question, QuestionAdmin)

# Now register the new UserAdmin...
admin.site.register(Voter, VoterAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)