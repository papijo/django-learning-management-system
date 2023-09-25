from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import reverse

from main.managers import UserManager


import cloudinary.models


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.
    """

    email = models.EmailField(unique=True, help_text="Enter Email address.")
    first_name = models.CharField(max_length=30, blank=True, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        """
        String representation of the user.
        """
        return self.email

    def get_full_name(self):
        """
        Returns the full name of the User.
        """
        fullname = f"{self.first_name} {self.last_name}"
        return fullname.strip()

    # def test_email_user(self, subject, message, from_email=None, **kwargs):
    #     """
    #     Sends a test email to this user.
    #     """
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class BioData(models.Model):
    """
    User's additional biographical data.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(
        null=True, blank=True, help_text="User's date of birth."
    )
    address = models.CharField(max_length=100, help_text="User's address.")
    phone_number = models.CharField(
        max_length=11, unique=True, help_text="User's phone number."
    )
    avatar = models.ImageField(
        upload_to="uploads/users/", null=True, blank=True, help_text="User's avatar."
    )
    next_of_kin = models.CharField(max_length=100, help_text="User's next of kin.")
    next_of_kin_phone_number = models.CharField(
        max_length=11, help_text="Next of kin's phone number."
    )

    class Meta:
        ordering = ["user"]

    def get_absolute_url(self):
        """
        Returns the URL for the user's biographical data.
        """
        return reverse("user-bio", args=[str(self.id)])


class Course(models.Model):
    """
    In-house courses offered by MSTC.
    """

    title = models.CharField(max_length=100, help_text="Title of the course.")
    description = models.CharField(
        max_length=100, help_text="Description of the course."
    )

    def __str__(self):
        """
        String representation of the course.
        """
        return self.title


class Subject(models.Model):
    """
    Academic subjects.
    """

    title = models.CharField(max_length=100, help_text="Title of the subject.")
    description = models.CharField(
        max_length=100, help_text="Description of the subject."
    )
    code = models.CharField(
        max_length=6, primary_key=True, help_text="Unique code for the subject."
    )
    course = models.ManyToManyField(Course, help_text="Courses related to the subject.")

    class Meta:
        ordering = ["title", "code"]

    def __str__(self):
        """
        String representation of the subject.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL for the subject's details.
        """
        return reverse("subject-detail", args=[str(self.code)])

    def display_course(self):
        """
        Returns a comma-separated list of related courses.
        """
        return ", ".join(course.title for course in self.course.all()[:3])

    display_course.short_description = "Course"


class LearningMaterial(models.Model):
    """
    Educational materials.
    """

    title = models.CharField(
        max_length=100, help_text="Title of the learning material."
    )
    description = models.CharField(
        max_length=100, help_text="Description of the learning material."
    )
    subject = models.OneToOneField(
        Subject, on_delete=models.CASCADE, help_text="Subject related to the material."
    )
    file = models.FileField(
        upload_to="uploads/learningmaterial",
        null=True,
        blank=True,
        help_text="File attachment.",
    )

    class Meta:
        ordering = ["title", "subject"]

    def __str__(self):
        """
        String representation of the learning material.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL for the learning material's details.
        """
        return reverse("learning-material-detail", args=[str(self.id)])


class Major(models.Model):
    """
    Courses done by interns at their educational institution.
    """

    name = models.CharField(max_length=100, help_text="Name of the major.")
    slug = models.SlugField(max_length=10)

    def __str__(self):
        """
        String representation of the major.
        """
        return self.name


class Laboratory(models.Model):
    """
    Educational institution laboratories.
    """

    name = models.CharField(max_length=100, help_text="Name of the laboratory.")
    slug = models.SlugField(max_length=10)

    class Meta:
        verbose_name = "Laboratory"
        verbose_name_plural = "Laboratories"

    def __str__(self):
        """
        String representation of the laboratory.
        """
        return self.name


class StudentProfile(models.Model):
    """
    Profiles for students.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(
        max_length=6, primary_key=True, help_text="Unique student ID."
    )
    course_start_date = models.DateField(help_text="Start date of the course.")
    course_end_date = models.DateField(help_text="End date of the course.")
    courses = models.ManyToManyField(
        Course, help_text="Courses associated with the student."
    )

    class Meta:
        ordering = ["user", "student_id"]

    def get_absolute_url(self):
        """
        Returns the URL for the student's profile.
        """
        return reverse("student_profile", args=[str(self.student_id)])

    def display_course(self):
        """
        Returns a comma-separated list of associated courses.
        """
        return ", ".join(course.title for course in self.courses.all()[:3])

    display_course.short_description = "Course"


class InstructorProfile(models.Model):
    """
    Profiles for instructors.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(
        max_length=6, primary_key=True, help_text="Unique staff ID."
    )

    def get_absolute_url(self):
        """
        Returns the URL for the teacher's profile.
        """
        return reverse("instructor_profile", args=[str(self.staff_id)])


class AdminProfile(models.Model):
    """
    Profiles for administrators.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(
        max_length=6, primary_key=True, help_text="Unique staff ID."
    )

    def get_absolute_url(self):
        """
        Returns the URL for the admin's profile.
        """
        return reverse("admin_profile", args=[str(self.staff_id)])


class EducationalInstitution(models.Model):
    """
    Educational institutions.
    """

    name = models.CharField(
        max_length=100, help_text="Name of the educational institution."
    )
    slug = models.SlugField(max_length=10)

    def __str__(self):
        """
        String representation of the educational institution.
        """
        return self.name


class InternProfile(models.Model):
    """
    Profiles for interns.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intern_id = models.CharField(
        max_length=6, primary_key=True, help_text="Unique intern ID."
    )
    internship_start_date = models.DateField(help_text="Start date of the internship.")
    internship_end_date = models.DateField(help_text="End date of the internship.")
    educational_institution = models.ForeignKey(
        EducationalInstitution,
        on_delete=models.CASCADE,
        help_text="Educational institution of the intern.",
    )
    laboratory_attached = models.ForeignKey(
        Laboratory,
        on_delete=models.CASCADE,
        help_text="Laboratory attached to the intern.",
    )
    course = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,
        help_text="Major course associated with the intern.",
    )

    def get_absolute_url(self):
        """
        Returns the URL for the intern's profile.
        """
        return reverse("intern_profile", args=[str(self.intern_id)])


class Assessment(models.Model):
    """
    Student assessments for subjects.
    """

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, help_text="Subject being assessed."
    )
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, help_text="Student being assessed."
    )
    date = models.DateField(help_text="Date of assessment.")
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Assessment grade."
    )
    comments = models.TextField(
        blank=True, null=True, help_text="Additional comments on the assessment."
    )

    ASSESSMENT_TYPES = [
        ("quiz", "Quiz"),
        ("exam", "Exam"),
        ("assignment", "Assignment"),
    ]
    assessment_type = models.CharField(
        max_length=20, choices=ASSESSMENT_TYPES, help_text="Type of assessment."
    )

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        """
        String representation of the assessment.
        """
        return f"{self.subject} - {self.student} - {self.get_assessment_type_display()}"

    def get_absolute_url(self):
        """
        Returns the URL for the assessment's details.
        """
        return reverse("assessment-detail", args=[str(self.id)])


class Task(models.Model):
    """
    Tasks assigned to interns by teachers.
    """

    assigner = models.ForeignKey(
        InstructorProfile,
        on_delete=models.CASCADE,
        help_text="Teacher assigning the task.",
    )
    assignee = models.ForeignKey(
        InternProfile,
        on_delete=models.CASCADE,
        help_text="Intern to whom the task is assigned.",
    )
    activity = models.TextField(
        blank=False, null=False, help_text="Description of the task."
    )
    date_assigned = models.DateField(help_text="Date when the task was assigned.")
    date_completed = models.DateField(help_text="Date when the task was completed.")

    STATUS_CHOICES = [("pending", "Pending"), ("completed", "Completed")]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        blank=False,
        default="pending",
        help_text="Status of the task.",
    )

    def get_absolute_url(self):
        """
        Returns the URL for the assessment's details.
        """
        return reverse("task-detail", args=[str(self.id)])
