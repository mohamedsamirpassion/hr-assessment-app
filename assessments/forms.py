from django import forms
from .models import Assessment, Question

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'duration': forms.NumberInput(attrs={'min': 1})
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type', 'text', 'points', 'options', 'correct_answer']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'options': forms.Textarea(attrs={'rows': 3, 'placeholder': '{"choices": ["Option 1", "Option 2"]}'}),
            'correct_answer': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_options(self):
        options = self.cleaned_data.get('options')
        if self.cleaned_data.get('type') == 'MC' and not options:
            raise forms.ValidationError("Options are required for multiple choice questions")
        return options