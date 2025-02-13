from django.db import models
from django.core.exceptions import ValidationError
from hr.models import HRProfile
from candidates.models import CandidateProfile

class Assessment(models.Model):
    hr = models.ForeignKey(HRProfile, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.hr.company}"

    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('COD', 'Coding Problem'),
        ('FB', 'Fill in the Blank'),
        ('ES', 'Essay'),
    ]

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=4, choices=QUESTION_TYPES)
    text = models.TextField()
    points = models.PositiveIntegerField(default=1)
    options = models.JSONField(
        blank=True, 
        null=True,
        help_text="For multiple choice: JSON format with 'choices' array. Example: {'choices': ['Yes', 'No']}"
    )
    correct_answer = models.TextField(blank=True)

    def clean(self):
        """Enhanced validation for question logic"""
        if self.type == 'MC':
            # Validate options structure
            if not self.options or not isinstance(self.options, dict):
                raise ValidationError({'options': 'Multiple choice questions require a dictionary with "choices" array'})
            
            if 'choices' not in self.options:
                raise ValidationError({'options': 'Missing required "choices" array in options'})
            
            if len(self.options.get('choices', [])) < 2:
                raise ValidationError({'options': 'At least two choices are required'})
            
            # Validate correct answer matches options
            if self.correct_answer not in self.options.get('choices', []):
                raise ValidationError({
                    'correct_answer': 'Must exactly match one of the provided options'
                })

        elif self.type == 'TF':
            # Enforce True/False answers
            if self.correct_answer.lower() not in ['true', 'false']:
                raise ValidationError({
                    'correct_answer': 'Must be "True" or "False" (case-insensitive)'
                })

        super().clean()

    def __str__(self):
        return f"{self.get_type_display()} Question: {self.text[:50]}..."

    class Meta:
        ordering = ['id']

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='answers',
        null=True,
        blank=True
    )
    response = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.text[:50]} by {self.candidate.user.email if self.candidate else 'Anonymous'}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Candidate Answer"