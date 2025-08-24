from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import JobSeekerProfileForm, EmployerProfileForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == "employer":
            return redirect("employer_dashboard")
        else:
            return redirect("job_seeker_dashboard")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.user_type == "employer":
                return redirect("employer_dashboard")
            else:
                return redirect("job_seeker_dashboard")
    return render(request, "job_nest/pages/auth/login_page.html")

def register_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == "employer":
            return redirect("employer_dashboard")
        else:
            return redirect("job_seeker_dashboard")
        
    if request.method == "POST":
        job_seeker_form = JobSeekerProfileForm()
        employer_form = EmployerProfileForm()
        user_type = request.POST.get("user_type")
        user = CustomUser(
            user_type=user_type,
            full_name=request.POST.get("full_name"),
            username=request.POST.get("username"),
            email=request.POST.get("email"),
        )
        user.set_password(request.POST.get("password"))
        if user:
            user.save()
            login(request, user)
            if user_type == "job-seeker":
                job_seeker_form = JobSeekerProfileForm(request.POST, request.FILES)
                if job_seeker_form.is_valid():
                    job_seeker_profile = job_seeker_form.save(commit=False)
                    job_seeker_profile.user = user
                    job_seeker_profile.save()
                    return redirect("job_seeker_dashboard")
            else:
                employer_form = EmployerProfileForm(request.POST, request.FILES)
                if employer_form.is_valid():
                    employer_profile = employer_form.save(commit=False)
                    employer_profile.user = user
                    employer_profile.save()
                    return redirect("employer_dashboard")
    else:
        job_seeker_form = JobSeekerProfileForm()
        employer_form = EmployerProfileForm()
    return render(request, "job_nest/pages/auth/register_page.html")

@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("home")