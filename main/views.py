from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


from .models import (
    StudentProfile,
    InstructorProfile,
    AdminProfile,
    InternProfile,
    BioData,
)
from .forms import (
    StudentProfileForm,
    InstructorProfileForm,
    AdminProfileForm,
    InternProfileForm,
    CustomUserCreationForm,
    UserBioDataForm,
)

from learning_management_system import settings


# Create your views here.


# Home Page
@login_required
def index(request):
    "Home Page of the Learning Management System"

    return render(request, "index.html")


# Registration View
class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        # Save the user but do not log them in
        user = form.save(commit=False)

        # Customize any additional user fields as needed
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]

        # Generate a random password (you can also allow users to set their password)
        # Configure later
        # user_password = user.set_unusable_password()

        # Save the user with the generated password
        user.save()

        # Send registration email to the user

        return super().form_valid(form)


# class UserRegistrationView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = "registration/registration_form.html"
#     success_url = reverse_lazy("index")

#     def form_valid(self, form):
#         # Save the user but do not log them in
#         user = form.save(commit=False)

#         # Customize any additional user fields as needed
#         user.first_name = form.cleaned_data["first_name"]
#         user.last_name = form.cleaned_data["last_name"]
#         user.email = form.cleaned_data["email"]

#         try:
#             # Generate a random password for the user
#             # user.set_password(get_user_model().objects.make_random_password())
#             user.save()

#             # Send registration email to the user
#             subject = f"Welcome to LMS, {user.last_name} {user.first_name}"
#             message = "Thank you for registering on our website. You can now log in."
#             from_email = settings.SMTP_EMAIL_SENDER

#             user.test_email_user(subject, message, from_email, fail_silently=False)

#             return super().form_valid(form)

#         except ValidationError as e:
#             # Handle validation errors if any occur during password generation
#             form.add_error(None, str(e))
#             return self.form_invalid(form)


# class CreateUserBioDataView(LoginRequiredMixin, CreateView):
#     model = BioData
#     form_class = UserBioDataForm
#     template_name = "registration/biodata_form.html"
#     success_url = reverse_lazy(
#         "index"
#     )  # Redirect to Profile creation page when bio data page is created.

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_queryset(self):
#         return BioData.objects.filter(user=self.request.user)


class CreateUserBioDataView(LoginRequiredMixin, CreateView):
    model = BioData
    form_class = UserBioDataForm
    template_name = "registration/biodata_form.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        # Check if a bio data entry already exists for the user
        existing_bio_data = BioData.objects.filter(user=self.request.user).exists()
        if existing_bio_data:
            raise ValidationError("You have already added bio data.")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Redirect if bio data entry already exists for the user
        if BioData.objects.filter(user=self.request.user).exists():
            return redirect("index")  # Redirect later to bio-data profile page
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if a bio data entry already exists for the user
        user_has_bio_data = BioData.objects.filter(user=self.request.user).exists()
        context["user_has_bio_data"] = user_has_bio_data
        return context


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
