from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("faq/", views.faq_view, name="faq"),
    path("browse-jobs", views.browse_jobs_view, name="browse_jobs"),
    path("post-job/", views.post_job_view, name="post_job"),
    path("apply-job/", views.apply_job_view, name="apply_job"),
    path("dashboard/", views.dashboard_view, name="dashboard")
]