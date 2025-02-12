from django import forms
from .models import Assessment, Question, Answer

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'duration': forms.NumberInput(attrs={'min': 1})
        }

class QuestionForm(forms.ModelForm):
    options = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter options separated by commas (e.g., Yes, No, Maybe)'
        }),
        help_text="For multiple choice questions only"
    )

    class Meta:
        model = Question
        fields = ['type', 'text', 'points', 'options', 'correct_answer']
        widgets = {
            'options': forms.TextInput(attrs={
                'placeholder': 'Enter options as comma-separated values (e.g., "Option 1, Option 2")'
            }),
            'correct_answer': forms.TextInput(attrs={
                'placeholder': 'Enter the correct answer (matching exactly one option for MC)'
            }),
        }
        help_texts = {
            'options': 'For multiple choice: separate options with commas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.options:
            self.initial['options'] = ', '.join(self.instance.options.get('choices', []))

    def clean_options(self):
        options = self.cleaned_data.get('options')
        if self.cleaned_data.get('type') == 'MC':
            if not options:
                raise forms.ValidationError("Options are required for multiple choice questions")
            try:
                options_list = [opt.strip() for opt in options.split(',') if opt.strip()]
                return {'choices': options_list}
            except Exception:
                raise forms.ValidationError("Enter options as: Option 1, Option 2, ...")
        return options

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['response', 'is_correct']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 2}),
        }