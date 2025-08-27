from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("faq/", views.faq_view, name="faq"),
    path("post-job/", views.post_job_view, name="post_job"),
    path("apply-job/", views.apply_job_view, name="apply_job"),
    path("employer/dashboard/", views.employer_dashboard_view, name="employer_dashboard"),
    path("job-seeker/dashboard/", views.job_seeker_dashboard_view, name="job_seeker_dashboard"),
    path("job-seeker/profile/", views.job_seeker_profile_view, name="job_seeker_profile"),
    path("apply-job/<str:pk>/", views.apply_job_view, name="apply_job"),
    path("job-seeker/applications/", views.all_job_seeker_applications, name="all_job_seeker_applications"),
    path("browse-jobs/", views.all_jobs_view, name="all_jobs"),
    path("job/<str:pk>/", views.job_details_view, name="job_details"),
    path("employer/profile/", views.employer_profile_view, name="employer_profile"),
    path("404/", views.fallback_page_view, name="404"),
    path("employer/profile/edit/", views.employer_profile_edit_view, name="employer_profile_edit"),
    path("employer/job-applications/", views.employer_all_job_applications, name="all_applications")
]