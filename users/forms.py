from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Custom user registration form extending the default UserCreationForm
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Form for updating user information
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']