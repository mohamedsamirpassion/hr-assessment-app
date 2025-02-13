from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=255,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    is_hr = models.BooleanField(
        default=False,
        verbose_name='HR Status',
        help_text='Designates whether this user is an HR professional'
    )
    is_candidate = models.BooleanField(
        default=False,
        verbose_name='Candidate Status',
        help_text='Designates whether this user is a job candidate'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        if self.is_hr and self.is_candidate:
            raise ValueError("User cannot be both HR and Candidate")
        super().save(*args, **kwargs)

class HRProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='hr_profile',
        limit_choices_to={'is_hr': True}
    )
    company = models.CharField(
        max_length=100,
        help_text='Company the HR represents'
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        help_text='HR position in the company'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text='Department within the company'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text='Contact phone number'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HR Profile'
        verbose_name_plural = 'HR Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.company}'

    def is_active_hr(self):
        return self.user.is_active