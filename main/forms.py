# forms.py
from django import forms
from .models import (
    StudentProfile,
    InstructorProfile,
    AdminProfile,
    InternProfile,
    User,
    BioData,
)
from django.contrib.auth.forms import UserCreationForm


# User Creation Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User  # Replace 'User' with your user model if different
        fields = ("first_name", "last_name", "email", "password1", "password2")


# Bio Data Creation Form
class UserBioDataForm(forms.ModelForm):
    class Meta:
        model = BioData
        fields = "__all__"  # Add or customize fields as needed


# Profile Creation Form
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"  # Add or customize fields as needed


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = "__all__"  # Add or customize fields as needed


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = "__all__"  # Add or customize fields as needed


class InternProfileForm(forms.ModelForm):
    class Meta:
        model = InternProfile
        fields = "__all__"  # Add or customize fields as needed
