from dataclasses import field
from django.contrib.auth.forms import UserCreationForm

from Publication.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", )