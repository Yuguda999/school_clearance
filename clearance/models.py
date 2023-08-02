from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Fee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    department = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    session = models.CharField(max_length=100)

class Student(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(null=True, max_length=255)
    matric_number = models.CharField(max_length=100, null=True)
    session = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    faculty = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    status = models.BooleanField(default=False)
    total_fee_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)

    # photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    
    def __str__(self):
        return self.username




class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    Payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



    def __str__(self):
        return f"{self.student} - ${self.amount}"



