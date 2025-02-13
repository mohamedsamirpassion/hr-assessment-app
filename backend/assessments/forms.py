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
        
        # Initialize options field for existing instances
        if self.instance and self.instance.options:
            # Handle both dictionary (MC) and string (non-MC) formats
            if isinstance(self.instance.options, dict) and 'choices' in self.instance.options:
                self.initial['options'] = ', '.join(self.instance.options['choices'])
            else:
                # Handle string format or invalid data gracefully
                self.initial['options'] = str(self.instance.options)

    def clean_options(self):
        options = self.cleaned_data.get('options', '')
        question_type = self.cleaned_data.get('type')

        if question_type == 'MC':
            # Validate and convert comma-separated string to dictionary
            if not options.strip():
                raise forms.ValidationError("Options are required for multiple choice questions.")
            
            try:
                options_list = [opt.strip() for opt in options.split(',') if opt.strip()]
                if len(options_list) < 2:
                    raise forms.ValidationError("At least two options are required for multiple choice.")
                
                return {'choices': options_list}
                
            except Exception as e:
                raise forms.ValidationError(f"Invalid options format: {str(e)}")
        
        # For non-MC questions, return empty string or raw value
        return options.strip() if options else ''

    def clean_correct_answer(self):
        question_type = self.cleaned_data.get('type')
        correct_answer = self.cleaned_data.get('correct_answer')
        options = self.cleaned_data.get('options')

        if question_type == 'MC' and isinstance(options, dict):
            if correct_answer not in options.get('choices', []):
                raise forms.ValidationError("Correct answer must match one of the provided options.")
        
        return correct_answer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['response', 'is_correct']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 2}),
        }