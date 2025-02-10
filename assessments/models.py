from django.db import models
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
    options = models.JSONField(blank=True, null=True, help_text="For multiple choice: {'choices': ['Option 1', 'Option 2']}")
    correct_answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_type_display()} Question - {self.text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    response = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.text[:50]} by {self.candidate.user.username if self.candidate else 'N/A'}"