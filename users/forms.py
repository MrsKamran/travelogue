from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    # current_user = request.user
    # print(current_user)


    class Meta:
        model = User
        fields = ['username', 'email']
