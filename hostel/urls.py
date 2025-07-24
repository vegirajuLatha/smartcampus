from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hostel_dashboard, name='hostel_dashboard'),
    path('dashboard/', views.hostel_dashboard, name='hostel-dashboard'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),  # ✅ matches the template
    path('penalties/', views.view_penalties, name='view_penalties'),


    # Admin views
    path('view-complaints/', views.view_complaints, name='view_complaints'),
    path('add-penalty/', views.add_penalty, name='add_penalty'),
    path('add-visitor/', views.add_visitor, name='add_visitor'),
    path('view-students/', views.view_students, name='view_students'),
    path('view-visitors/', views.view_visitors, name='view_visitors'),

    path('add-penalty/', views.add_penalty, name='add_penalty'),
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='hostel-admin-dashboard'),
    path('hostel/dashboard/', views.dashboard_redirect, name='dashboard-redirect'),
    path('hostel/admin/', views.admin_dashboard, name='hostel-admin-dashboard'),
    path('hostel/student/', views.student_dashboard, name='student-dashboard'),
]
