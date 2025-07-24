from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="management_student")
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    

    def __str__(self):
        return self.user.get_full_name()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"


class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    marks_obtained = models.FloatField()
    max_marks = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.subject}"

class StudentDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
