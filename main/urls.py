from django.urls import path
from .views import (
    index,
    StudentProfileCreateView,
    InstructorProfileCreateView,
    AdminProfileCreateView,
    InternProfileCreateView,
    UserRegistrationView,
    UserBioDataView,
)


urlpatterns = [
    # Home Route
    path("", index, name="index"),
    # Profile Routes
    path(
        "create/student/",
        StudentProfileCreateView.as_view(),
        name="create-student-profile",
    ),
    path(
        "create/instructor/",
        InstructorProfileCreateView.as_view(),
        name="create-instructor-profile",
    ),
    path(
        "create/admin/",
        AdminProfileCreateView.as_view(),
        name="create-admin-profile",
    ),
    path(
        "create/intern/",
        InternProfileCreateView.as_view(),
        name="create-intern-profile",
    ),
    # Bio Data Route
    path("create/biodata/", UserBioDataView.as_view(), name="biodata"),
    # LMS Auth Routes
    path("register/", UserRegistrationView.as_view(), name="register"),
]
