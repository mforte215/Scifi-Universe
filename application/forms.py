from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Comment, Member


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Member
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["article", "commentor"]

class SearchForm(forms.Form):
    search_input = forms.CharField(max_length=250, label='Search')
    