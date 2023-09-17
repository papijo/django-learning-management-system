from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("Email is required to create a user.")

        # Normalize the email (convert to lowercase)
        email = self.normalize_email(email)

        # Create a new user instance with the provided email and any additional fields
        user = self.model(email=email, **extra_fields)

        # Set the password and save the user to the database
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        # Ensure is_staff and is_superuser are set to True
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Call the create_user method to create the superuser
        return self.create_user(email, password, **extra_fields)
