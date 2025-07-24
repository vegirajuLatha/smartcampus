from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student-dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('attendance/', views.view_attendance, name='view_attendance'),
    path('academics/', views.academic_performance, name='academic_performance'),
    path('documents/', views.upload_document, name='upload_document'),
    path('face-attendance/', views.face_attendance_page, name='face_attendance'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

