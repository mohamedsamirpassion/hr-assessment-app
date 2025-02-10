from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assessment, Question
from .forms import AssessmentForm, QuestionForm
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