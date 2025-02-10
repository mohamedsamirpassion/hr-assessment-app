from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
            return redirect('add_questions', assessment_id=assessment.id)
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
            question = form.save(commit=False)
            question.assessment = assessment
            question.save()
            return redirect('add_questions', assessment_id=assessment.id)
    else:
        form = QuestionForm()
    return render(request, 'assessments/add_questions.html', {
        'assessment': assessment,
        'form': form,
        'questions': assessment.questions.all()
    })

@login_required
def create_question(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, hr__user=request.user)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.assessment = assessment
            question.save()

            # Handle answers for multiple-choice questions
            if question.type == 'MC':  # Use 'MC' based on your QUESTION_TYPES in models
                answer_forms = [AnswerForm(request.POST, prefix=str(i)) for i in range(4)]
                if all(form.is_valid() for form in answer_forms):
                    for form in answer_forms:
                        answer = form.save(commit=False)
                        answer.question = question
                        answer.save()
                    return redirect('view_assessment', assessment_id=assessment.id)
            else:
                return redirect('view_assessment', assessment_id=assessment.id)
    else:
        question_form = QuestionForm()
        answer_forms = [AnswerForm(prefix=str(i)) for i in range(4)]  # Pre-fill 4 answer forms for MCQ

    context = {
        'question_form': question_form,
        'answer_forms': answer_forms,
        'assessment': assessment,
    }
    return render(request, 'assessments/create_question.html', context)

@login_required
def view_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, hr__user=request.user)
    questions = assessment.questions.all()
    return render(request, 'assessments/view_assessment.html', {
        'assessment': assessment,
        'questions': questions
    })