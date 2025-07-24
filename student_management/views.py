from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Attendance, AcademicRecord, StudentDocument
from .forms import StudentDocumentForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance
from datetime import date
from deepface import DeepFace
from PIL import Image
import numpy as np
import cv2

@login_required
def student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('student-dashboard')
    return render(request, 'student_management/profile.html', {'student': student})

from django.contrib.auth.decorators import login_required

@login_required
def view_attendance(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('some-error-page-or-dashboard')

    records = Attendance.objects.filter(student=student).order_by('-date')
    
    return render(request, 'student_management/attendance.html', {'records': records})


@login_required
def academic_performance(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact admin.")
        return redirect('student_dashboard')

    records = AcademicRecord.objects.filter(student=student)

    # Add percentage calculation
    performance = []
    for r in records:
        percentage = (r.marks_obtained / r.max_marks) * 100 if r.max_marks > 0 else 0
        performance.append({
            'semester': r.semester,
            'subject': r.subject,
            'marks_obtained': r.marks_obtained,
            'max_marks': r.max_marks,
            'percentage': round(percentage, 2)
        })

    return render(request, 'student_management/academic.html', {'performance': performance})

@login_required
def upload_document(request):
    student = Student.objects.get(user=request.user)
    documents = StudentDocument.objects.filter(student=student)

    if request.method == 'POST':
        form = StudentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = student
            doc.save()
            return redirect('upload_document')
    else:
        form = StudentDocumentForm()

    return render(request, 'student_management/upload_document.html', {
        'form': form,
        'documents': documents,
    })

from django.contrib.auth.decorators import login_required
from django.utils import timezone
@login_required
def student_dashboard(request):
    today = timezone.now().date()

    # Mark Absent only once per day
    if not Attendance.objects.filter(date=today, status='Absent').exists():
        students = Student.objects.all()
        for student in students:
            already_marked = Attendance.objects.filter(student=student, date=today).exists()
            if not already_marked:
                Attendance.objects.create(student=student, date=today, status='Absent')

    return render(request, 'student_management/dashboard.html')

@login_required
def face_attendance_page(request):
    return render(request, 'student_management/face_attendance.html')


@csrf_exempt
@login_required
def mark_attendance(request):
    if request.method == 'POST' and request.FILES.get('live_image'):
        try:
            student = Student.objects.get(user=request.user)
            reference_image = cv2.imread(student.photo.path)
            live_file = request.FILES['live_image']
            live_image = np.array(Image.open(live_file).convert('RGB'))

            result = DeepFace.verify(live_image, reference_image, enforce_detection=False)

            # Get or create attendance record for today
            attendance_record, created = Attendance.objects.get_or_create(
                student=student,
                date=date.today()
            )

            if result["verified"]:
                attendance_record.status = 'Present'
                attendance_record.save()
                return JsonResponse({'message': '✅ Face matched. Attendance marked as Present.'})
            else:
                attendance_record.status = 'Absent'
                attendance_record.save()
                return JsonResponse({'message': '❌ Face does not match. Marked as Absent.'}, status=400)

        except Exception as e:
            return JsonResponse({'message': f'⚠️ Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)
