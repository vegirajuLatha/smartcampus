from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutor_home, name='tutor_home'),
    path('chat/', views.chat_interface, name='chat_interface'),
    path('upload/', views.upload_notes, name='upload_notes'),
]
