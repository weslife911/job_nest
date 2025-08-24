from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from users.models import EmployerProfile, CustomUser

# Create your views here.
def home_view(request):
    return render(request, "job_nest/pages/guest/home_page.html")

def about_view(request):
    return render(request, "job_nest/pages/guest/about_page.html")

def contact_view(request):
    return render(request, "job_nest/pages/guest/contact_page.html")

def faq_view(request):
    return render(request, "job_nest/pages/guest/faq_page.html")

@login_required(login_url="login")
def browse_jobs_view(request):
    return render(request, "job_nest/pages/jobs/browse_jobs_page.html")

@login_required(login_url="login")
def post_job_view(request):
    if request.user.user_type != "employer":
        return redirect("job_seeker_dashboard")

    if request.method == "POST":
        job = Job.objects.create(
            employer_id=request.user.id,
            job_title=request.POST.get("job_title"),
            job_type=request.POST.get("job_type"),
            salary=request.POST.get("salary"),
            job_description=request.POST.get("job_description")
        )
        if job:
            job.save()
            return redirect("employer_dashboard")

    return render(request, "job_nest/pages/jobs/post_job_page.html")
    

@login_required(login_url="login")
def apply_job_view(request):
    return render(request, "job_nest/pages/jobs/apply_job_page.html")

@login_required(login_url="login")
def employer_dashboard_view(request):
    if request.user.user_type == "employer":
        jobs = Job.objects.all()
        employer = EmployerProfile.objects.get(user=request.user)
        return render(request, "job_nest/pages/user/employer/dashboard.html", {"jobs": jobs, "employer": employer})
    else:
        return redirect("job_seeker_dashboard")

@login_required(login_url="login")
def job_seeker_dashboard_view(request):
    if request.user.user_type == "job-seeker":
        return render(request, "job_nest/pages/user/job_seeker/dashboard.html")
    else:
        return redirect("employer_dashboard")