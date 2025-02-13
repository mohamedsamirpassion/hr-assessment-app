from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assessment, Question, Answer
from .forms import AssessmentForm, QuestionForm, AnswerForm
from hr.models import HRProfile

@login_required
def create_assessment(request):
    hr_profile = get_object_or_404(HRProfile, user=request.user)
    
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.hr = hr_profile
            assessment.save()
            messages.success(request, 'Assessment created successfully!')
            return redirect('add_questions', assessment_id=assessment.id)
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = AssessmentForm()
    
    assessments = Assessment.objects.filter(hr=hr_profile)
    return render(request, 'assessments/create_assessment.html', {
        'form': form,
        'assessments': assessments
    })

@login_required
def add_questions(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, hr__user=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            try:
                question = form.save(commit=False)
                question.assessment = assessment

                # Convert comma-separated options to JSON format
                if question.type == 'MC' and form.cleaned_data.get('options'):
                    options = [opt.strip() for opt in form.cleaned_data['options'].split(',')]
                    question.options = {'choices': options}

                question.save()
                messages.success(request, 'Question added successfully!')
                return redirect('add_questions', assessment_id=assessment.id)
            except Exception as e:
                messages.error(request, f'Error saving question: {str(e)}')
        else:
            # Show form errors in messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    
    else:
        form = QuestionForm()

    questions = assessment.questions.all().order_by('-id')
    return render(request, 'assessments/add_questions.html', {
        'assessment': assessment,
        'form': form,
        'questions': questions
    })

@login_required
def create_question(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, hr__user=request.user)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(i)) for i in range(4)]
        
        if question_form.is_valid() and all(f.is_valid() for f in answer_forms):
            try:
                # Save question
                question = question_form.save(commit=False)
                question.assessment = assessment
                question.save()
                
                # Save answers for MCQs
                if question.type == 'MC':
                    for form in answer_forms:
                        answer = form.save(commit=False)
                        answer.question = question
                        answer.save()
                
                messages.success(request, 'Question and answers saved successfully!')
                return redirect('view_assessment', assessment_id=assessment.id)
                
            except Exception as e:
                messages.error(request, f'Error saving question: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below')
    
    else:
        question_form = QuestionForm()
        answer_forms = [AnswerForm(prefix=str(i)) for i in range(4)]

    return render(request, 'assessments/create_question.html', {
        'question_form': question_form,
        'answer_forms': answer_forms,
        'assessment': assessment
    })

@login_required
def view_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, hr__user=request.user)
    questions = assessment.questions.all().prefetch_related('answer_set')
    
    return render(request, 'assessments/view_assessment.html', {
        'assessment': assessment,
        'questions': questions
    })