from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request):
    return render(request, "job_nest/pages/home_page.html")

def about_view(request):
    return render(request, "job_nest/pages/about_page.html")

def contact_view(request):
    return render(request, "job_nest/pages/contact_page.html")

def faq_view(request):
    return render(request, "job_nest/pages/faq_page.html")


def browse_jobs_view(request):
    return render(request, "job_nest/pages/browse_jobs_page.html")

def post_job_view(request):
    return render(request, "job_nest/pages/post_job_page.html")

def apply_job_view(request):
    return render(request, "job_nest/pages/apply_job_page.html")