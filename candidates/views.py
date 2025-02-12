from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import CandidateProfile

def candidate_login(request):
    if request.user.is_authenticated and request.user.is_candidate:
        return redirect('candidate_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_candidate:
            login(request, user)
            return redirect('candidate_dashboard')
        else:
            messages.error(request, 'Invalid credentials or unauthorized access')
    
    return render(request, 'candidates/login.html')

@login_required
def candidate_dashboard(request):
    if not request.user.is_candidate:
        return HttpResponseForbidden("Access denied")
    
    context = {
        'user': request.user,
        'profile': request.user.candidate_profile
    }
    return render(request, 'candidates/dashboard.html', context)

def candidate_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('candidate_login')