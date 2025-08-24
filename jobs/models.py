from django.db import models
from users.models import EmployerProfile

# Create your models here.

class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=300)
    job_type = models.CharField(max_length=100)
    salary = models.CharField(max_length=150)
    job_description = models.TextField(blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        if self.employer and self.employer.user:
            return f"{self.employer.user.username}'s position - {self.job_title}"
        return f"Job - {self.job_title}"
