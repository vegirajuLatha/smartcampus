from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='attendance_home'),  # Smart Campus home page
    path('login/', views.face_login, name='face_login'),  # Face login
    path('register/', views.register_face, name='register_face'),  # Register student face
    path('check/', views.check_attendance, name='check_attendance'),  # Check attendance via image
    path('recognize/', views.recognize_face, name='recognize_face'),  # Recognize face
]
