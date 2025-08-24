from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def login_view(request):
    return render(request, "job_nest/pages/login_page.html")

def register_view(request):
    return render(request, "job_nest/pages/register_page.html")

def logout_user(request):
    logout(request)
    return redirect("home")