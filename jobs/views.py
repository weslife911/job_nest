from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    return render(request, "job_nest/pages/jobs/post_job_page.html")

@login_required(login_url="login")
def apply_job_view(request):
    return render(request, "job_nest/pages/jobs/apply_job_page.html")

def dashboard_view(request):
    print(request.user)
    return render(request, "job_nest/pages/user/dashboard.html")