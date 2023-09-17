from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import StudentProfile, InstructorProfile, AdminProfile, InternProfile
from .forms import (
    StudentProfileForm,
    InstructorProfileForm,
    AdminProfileForm,
    InternProfileForm,
    CustomUserCreationForm,
)


# Create your views here.
def index(request):
    "Home Page of the Learning Management System"

    return render(request, "index.html")


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = (
        "registration/registration_form.html"  # Adjust the template path as needed
    )
    success_url = reverse_lazy(
        "index"
    )  # Redirect to bio-data page when bio data page is created.

    def form_valid(self, form):
        # Send email on successful registration
        # Log the user in after successful registration
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class StudentProfileCreateView(CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = "create_student_profile.html"
    success_url = reverse_lazy("index")  # Replace with a valid success URL


class InstructorProfileCreateView(CreateView):
    model = InstructorProfile
    form_class = InstructorProfileForm
    template_name = "create_instructor_profile.html"
    success_url = reverse_lazy("index")  # Replace with a valid success URL


class AdminProfileCreateView(CreateView):
    model = AdminProfile
    form_class = AdminProfileForm
    template_name = "create_admin_profile.html"
    success_url = reverse_lazy("index")  # Replace with a valid success URL


class InternProfileCreateView(CreateView):
    model = InternProfile
    form_class = InternProfileForm
    template_name = "create_intern_profile.html"
    success_url = reverse_lazy("index")  # Replace with a valid success URL
