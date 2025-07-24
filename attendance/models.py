from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    image_path = models.CharField(max_length=255)  # path to saved face image

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.date} {self.time}"


class SyllabusDocument(models.Model):
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_syllabus_docs')
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="syllabus/")

    def __str__(self):
        return self.title  # ✅ Display the title of the uploaded document
