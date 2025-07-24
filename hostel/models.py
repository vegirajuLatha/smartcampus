from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Student Profile linked to default Django User
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    hostel = models.CharField(max_length=100)
    room = models.CharField(max_length=10)
    

    def __str__(self):
        return self.user.username


class Complaint(models.Model):
    subject = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Add this
    is_resolved = models.BooleanField(default=False)      # ✅ Add this

    def __str__(self):
        return self.subject


class Visitor(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    purpose = models.TextField()
    visit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} visiting {self.student.user.username}"

class Penalty(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date_issued = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} visiting {self.student.user.username} for {self.purpose}"  # ✅ Corrected
