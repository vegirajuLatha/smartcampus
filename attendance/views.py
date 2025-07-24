import base64
import cv2
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from datetime import datetime
from .models import Student  # Make sure your Student model is defined properly


# 🔵 Main Smart Campus Home Page (with buttons)
def home_page(request):
    return render(request, 'attendance/home.html')


# 🟣 Attendance Module - Face Login Page
@csrf_exempt
def face_login(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        mode = request.POST.get('mode')
        justification = request.POST.get('justification')

        if image_data:
            format, imgstr = image_data.split(';base64,')
            image_bytes = base64.b64decode(imgstr)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # TODO: Add face recognition logic here

            print(f"Login at {datetime.now()} | Lat: {lat} | Lon: {lon} | Mode: {mode} | Justification: {justification}")

        return HttpResponse("Login Recorded")

    return render(request, 'attendance/face_login.html')


# 🧑‍🎓 Face Registration (Admin/Student Use)
@csrf_exempt
def register_face(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        image_data = request.POST.get('image_data')

        # Decode base64 image data
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{student_id}.{ext}')

        # Save or update the student with face image
        Student.objects.update_or_create(student_id=student_id, defaults={'image': data})

        return JsonResponse({'message': '✅ Face registered successfully'})

    return JsonResponse({'error': '❌ Invalid request method'})


# ✅ Check if a student is present
def check_attendance(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        # You can fetch actual attendance data from DB here
        return JsonResponse({'student_id': student_id, 'status': 'Present'})

    return JsonResponse({'error': 'Invalid request'})


# 🟢 Optional: Face Attendance Marking UI Page
def mark_attendance(request):
    return render(request, 'attendance/mark_attendance.html')


# 🔍 Recognize Face from Uploaded Image
@csrf_exempt
def recognize_face(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        if not image_data:
            return JsonResponse({'error': 'No image data received'})

        format, imgstr = image_data.split(';base64,')
        image_bytes = base64.b64decode(imgstr)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # TODO: Add real face recognition logic
        recognized = True  # Placeholder result

        if recognized:
            return JsonResponse({'status': 'Face recognized', 'name': 'John Doe'})
        else:
            return JsonResponse({'status': 'Face not recognized'})

    return JsonResponse({'error': 'Invalid request method'})
