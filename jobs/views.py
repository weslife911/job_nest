from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplied
from users.models import EmployerProfile, JobSeekerProfile, CustomUser
from users.forms import JobSeekerProfileForm
from django.http import Http404
from django.contrib import messages
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string

# Create your views here.
def home_view(request):
    return render(request, "job_nest/pages/guest/home_page.html")

def about_view(request):
    return render(request, "job_nest/pages/guest/about_page.html")

def contact_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if subject and message and full_name and email:
            try:
                # Validate email format
                validate_email(email)

                context = {
                    "full_name": full_name,
                    "email": email,
                    "subject": subject,
                    "message": message,
                }

                html_message = render_to_string(
                    "job_nest/pages/emails/contact_email.html", context
                )
                send_mail(
                    f"New Contact Form Submission: {subject}",
                    message,
                    email,
                    [settings.EMAIL_HOST_USER],
                    html_message=html_message,
                    fail_silently=False,
                )

                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')

            except ValidationError:
                messages.error(request, "Please enter a valid email address.")
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                messages.error(request, "An error occurred while sending your message. Please try again later.")
        else:
            messages.error(request, "All fields are required.")

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
        responsibilities = request.POST.getlist("responsibilities[]")
        qualifications = request.POST.getlist("qualifications[]")
        benefits = request.POST.getlist("benefits[]")
        try:
            responsibilities_json = json.dumps(responsibilities)
            qualifications_json = json.dumps(qualifications)
            benefits_json = json.dumps(benefits)
        except (TypeError, ValueError) as e:
            print(f"Error serializing data: {e}")
            return render(request, "job_nest/pages/user/employer/post_job_page.html", {'error_message': 'Invalid data format.'})
        job = Job.objects.create(
            employer_id=request.user.id,
            job_title=request.POST.get("job_title"),
            job_type=request.POST.get("job_type"),
            salary=request.POST.get("salary"),
            job_description=request.POST.get("job_description"),
            responsibilities=responsibilities_json,
            qualifications=qualifications_json,
            benefits=benefits_json
        )
        if job:
            job.save()
            return redirect("employer_dashboard")

    return render(request, "job_nest/pages/user/employer/post_job_page.html")
    

@login_required(login_url="login")
def employer_dashboard_view(request):
    if request.user.user_type != "employer":
        return redirect("job_seeker_dashboard")

    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect("404")
    
    jobs = Job.objects.filter(employer=employer).annotate(applicant_count=Count('jobapplied'))
    applications = JobApplied.objects.all()
    applications = applications[:2]

    context = {
        "jobs": jobs,
        "employer": employer,
        "applications": applications
    }

    return render(request, "job_nest/pages/user/employer/dashboard.html", context)

@login_required(login_url="login")
def job_seeker_dashboard_view(request):
    if request.user.user_type == "job-seeker":
        recommended_jobs = Job.objects.all()
        first_two_jobs = recommended_jobs[:2]
        job_applications = JobApplied.objects.all()
        first_two_applications = job_applications[:2]
        return render(request, "job_nest/pages/user/job_seeker/dashboard.html", {"jobs": first_two_jobs, "applications": first_two_applications})
    else:
        return redirect("employer_dashboard")

@login_required(login_url="login")
def job_seeker_profile_view(request):
    if request.user.user_type == "job-seeker":
        try:
            user = JobSeekerProfile.objects.get(user=request.user)
        except:
            raise Http404("Job seeker profile does not exist.")
        job_seeker_form = JobSeekerProfileForm(instance=user)
        if request.method == "POST":
            job_seeker_form = JobSeekerProfileForm(request.POST, request.FILES, instance=user)
            if job_seeker_form.is_valid():
                job_seeker_form.save()
                return redirect("job_seeker_profile")
        return render(request, "job_nest/pages/user/job_seeker/job_seeker_profile.html", {"user": user})
    else:
        return redirect("employer_dashboard")

@login_required(login_url="login")
def apply_job_view(request, pk):
    if request.user.user_type != "job-seeker":
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("employer_dashboard")

    job = get_object_or_404(Job, pk=pk)
    job_seeker_profile = CustomUser.objects.get(id=request.user.id)

    if JobApplied.objects.filter(job=job, job_seeker=job_seeker_profile).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_seeker_dashboard")

    if request.method == "POST":
        desired_salary = request.POST.get('desired_salary')
        availability = request.POST.get('availability')
        referral = request.POST.get('referral')
        cover_letter = request.POST.get('cover_letter')
        additional_notes = request.POST.get('additional_notes')

        try:
            JobApplied.objects.create(
                job=job,
                job_seeker=job_seeker_profile,
                desired_salary=desired_salary,
                availability=availability,
                referral=referral,
                cover_letter=cover_letter,
                additional_notes=additional_notes
            )
            messages.success(request, "Your application has been submitted successfully! 🎉")
            return redirect("job_seeker_dashboard")
        
        except IntegrityError:
            messages.error(request, "A database error occurred. Please try again.")
            return redirect("job_seeker_dashboard")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect("job_seeker_dashboard")

    context = {
        "job": job,
    }
    return render(request, "job_nest/pages/user/job_seeker/apply_job.html", context)

@login_required(login_url="login")
def all_job_seeker_applications(request):
    if request.user.user_type != "job-seeker":
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("employer_dashboard")
    applications = JobApplied.objects.filter(job_seeker_id=request.user.id)
    items_per_page = 5
    paginator = Paginator(applications, items_per_page)
    page_number = request.GET.get('page', 1)
    try:
        applications = paginator.page(page_number)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    return render(request, "job_nest/pages/user/job_seeker/all_job_seeker_applications.html", {"applications": applications})

@login_required(login_url="login")
def all_jobs_view(request):
    if request.user.user_type != "job-seeker":
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("employer_dashboard")
    job_title_query = request.GET.get("job_title")
    location_query = request.GET.get("location")
    job_type_query = request.GET.get("job_type")

    jobs = Job.objects.all()

    if job_title_query:
        jobs = jobs.filter(
            Q(job_title__icontains=job_title_query) | Q(employer__company_name__icontains=job_title_query)
        ).distinct()

    if location_query:
        jobs = jobs.filter(employer__company_location__icontains=location_query)

    if job_type_query and job_type_query != "Job Type":
        jobs = jobs.filter(job_type__icontains=job_type_query)
        
    paginator = Paginator(jobs, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "job_nest/pages/jobs/all_jobs.html", {"page_obj": page_obj})

@login_required(login_url="login")
def job_details_view(request, pk):
    job = get_object_or_404(Job, id=pk)
    
    try:
        job.responsibilities = json.loads(job.responsibilities) if job.responsibilities else []
        job.qualifications = json.loads(job.qualifications) if job.qualifications else []
        job.benefits = json.loads(job.benefits) if job.benefits else []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for job {pk}: {e}")
        job.responsibilities = []
        job.qualifications = []
        job.benefits = []

    context = {
        "job": job
    }
    return render(request, "job_nest/pages/jobs/job_details.html", context)

@login_required(login_url="login")
def employer_profile_view(request):
    employer = EmployerProfile.objects.get(user=request.user)
    jobs_list = Job.objects.filter(employer=employer).annotate(applicant_count=Count('jobapplied'))
    paginator = Paginator(jobs_list, 5)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)
    return render(request, "job_nest/pages/user/employer/employer_profile.html", {"employer": employer, "jobs": jobs})

def fallback_page_view(request):
    return render(request, "job_nest/pages/404/404.html")

@login_required(login_url="login")
def employer_profile_edit_view(request):
    if request.user.user_type != "employer":
        return redirect("job_seeker_dashboard")
    employer = EmployerProfile.objects.get(user=request.user)
    return render(request, "job_nest/pages/user/employer/employer_profile_edit_view.html", {"employer": employer})

@login_required(login_url="login")
def employer_all_job_applications(request):
    if request.user.user_type != "employer":
        return redirect("job_seeker_dashboard")
    employer = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer=employer)
    applications = JobApplied.objects.filter(job__in=jobs)
    return render(request, "job_nest/pages/user/employer/job_applications.html", {"applications": applications})