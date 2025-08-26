from django.db import models
from users.models import EmployerProfile, CustomUser
from django.core.validators import MinValueValidator

# Create your models here.

class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=300)
    job_type = models.CharField(max_length=100)
    salary = models.CharField(max_length=150)
    job_description = models.TextField(blank=True)
    
    # These fields will now store lists of strings
    responsibilities = models.JSONField(
        default=list, 
        help_text="A list of the job's key responsibilities."
    )
    qualifications = models.JSONField(
        default=list, 
        help_text="A list of required qualifications and skills."
    )
    benefits = models.JSONField(
        default=list, 
        help_text="A list of company benefits offered for the position."
    )
    
    JOB_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('interviewing', 'Interviewing'),
        ('completed', 'Completed'),
    ]
    job_status = models.CharField(
        max_length=20,
        choices=JOB_STATUS_CHOICES,
        default='active'
    )

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        if self.employer and self.employer.user:
            return f"{self.employer.user.username}'s job opening - {self.job_title}"
        return f"Job - {self.job_title}"


class JobApplied(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    desired_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    availability = models.DateField(blank=True, null=True)
    referral = models.CharField(max_length=50, blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)

    additional_notes = models.TextField(blank=True, null=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    class Meta:
        ordering = ['-updated', '-created']
        unique_together = ('job_seeker', 'job')

    def __str__(self):
        return f"{self.job_seeker.username} applied for {self.job.job_title}"
