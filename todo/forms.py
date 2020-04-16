from django.forms import ModelForm
from .models import Todo
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class TodoForm(ModelForm):
    """ Custom form to create a ToDo """
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    fullname = forms.CharField(label = "First name")
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ("username", "fullname", "email", )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        first_name, last_name = self.cleaned_data["fullname"].split()
        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
