from django.db import models


class User(models.Model):
    fullname = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=128)
    password = models.EmailField(unique=True)
    confirm_password = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_title}"
    
    @property
    def initials(self):
        
        return f"{self.first_name[0]}{self.last_name[0]}".upper()
