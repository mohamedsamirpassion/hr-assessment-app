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
        question_type = self.cleaned_data.get('type')
        
        # Validate options for multiple-choice questions
        if question_type == 'MC' and not options:
            raise forms.ValidationError("Options are required for multiple choice questions.")
        
        # Ensure options are in valid JSON format
        try:
            if options:
                options_dict = eval(options)  # Use eval to parse JSON-like string
                if not isinstance(options_dict, dict) or 'choices' not in options_dict:
                    raise ValueError()
        except Exception:
            raise forms.ValidationError("Options must be a valid JSON object with a 'choices' key.")
        
        return options

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['response', 'is_correct']  # Corrected field name from 'text' to 'response'
        widgets = {
            'response': forms.Textarea(attrs={'rows': 2}),  # Updated widget for 'response'
        }