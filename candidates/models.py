from django.db import models
from django.contrib.auth import get_user_model
from hr.models import User  # Import from hr app

class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='candidate_profile'
    )
    resume = models.FileField(
        upload_to='resumes/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text='Upload your resume in PDF format'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Contact Number'
    )
    linkedin_profile = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='LinkedIn Profile'
    )

    class Meta:
        verbose_name = 'Candidate Profile'
        verbose_name_plural = 'Candidate Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} Profile'