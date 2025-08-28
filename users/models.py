from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=[('job-seeker', 'Job Seeker'), ('employer', 'Employer')], default='job-seeker')
    full_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=100, unique=True)
    
    email = models.EmailField(unique=True, blank=False, null=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
    about = models.TextField(max_length=500, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    experience = models.PositiveSmallIntegerField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    linkedin_profile = models.URLField(max_length=200, blank=True)
    portfolio_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_profile = models.URLField(max_length=200, blank=True, null=True)
    x_profile = models.URLField(max_length=200, blank=True, null=True)
    instagram_profile = models.URLField(max_length=200, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"

class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    company_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    company_website = models.URLField(max_length=200, blank=True)
    company_size = models.CharField(max_length=20, blank=True)
    company_location = models.CharField(max_length=100, blank=True)
    
    industry = models.CharField(max_length=100, blank=True)
    company_mission = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_description = models.TextField(blank=True)
    
    def __str__(self):
        return self.company_name