from django.contrib import admin
from .models import (
    User,
    BioData,
    Course,
    Subject,
    LearningMaterial,
    Major,
    Laboratory,
    StudentProfile,
    InstructorProfile,
    AdminProfile,
    EducationalInstitution,
    InternProfile,
    Assessment,
    Task,
)

# Register your models here.


class BioDataInline(admin.StackedInline):
    model = BioData


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "get_full_name", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )
    inlines = [BioDataInline]


@admin.register(BioData)
class BioDataAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "address", "phone_number")
    list_filter = ("date_of_birth",)
    search_fields = ("user__email", "address", "phone_number")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "code", "display_course")
    list_filter = ("course",)
    search_fields = ("title", "description", "code")
    filter_horizontal = ("course",)


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "subject", "file")
    list_filter = ("subject",)
    search_fields = ("title", "description", "subject__title")


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "student_id",
        "course_start_date",
        "course_end_date",
        "display_course",
    )
    # list_filter = ("course",)
    search_fields = ("user__email", "student_id")
    filter_horizontal = ("courses",)


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "staff_id")


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "staff_id")


@admin.register(EducationalInstitution)
class EducationalInstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(InternProfile)
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "intern_id", "internship_start_date", "internship_end_date")
    list_filter = ("educational_institution", "laboratory_attached", "course")
    search_fields = ("user__email", "intern_id")


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("subject", "student", "date", "grade", "assessment_type")
    list_filter = ("subject", "student", "assessment_type")
    search_fields = ("subject__title", "student__user__email")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "assigner",
        "assignee",
        "activity",
        "date_assigned",
        "date_completed",
        "status",
    )
    list_filter = ("assigner", "assignee", "status")
    search_fields = ("assigner__user__email", "assignee__user__email", "activity")
