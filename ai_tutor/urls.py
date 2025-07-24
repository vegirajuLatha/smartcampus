# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dashboard, name='ai_tutor_dashboard'),
#     path('chat/', views.chat, name='chat'),
#     path('chat-api/', views.chat_api, name='chat_api'),
#     path('voice/', views.voice_input, name='voice_input'),
#     path('voice-api/', views.voice_api, name='voice_api'),  # ✅ New voice API route
#     path("ai-tutor/voice-input/", views.voice_input, name="voice_input"),
#     path('summarize/', views.summarize, name='summarize'),
#     path('quiz/', views.quiz_generator, name='quiz_generator'),
#     path('quiz-generator/', views.quiz_generator_view, name='quiz_generator'),  # Renders page (GET)
#     path('generate-quiz/', views.generate_quiz, name='generate_quiz'),
#     path('upload/', views.upload_syllabus, name='upload_syllabus'),
# ]

from django.urls import path
from . import views

# ai_tutor/urls.py


urlpatterns = [
    path('', views.dashboard, name='ai_tutor_dashboard'),
    path('chat/', views.chat, name='chat'),
    path('chat-api/', views.chat_api, name='chat_api'),
    path('voice/', views.voice_input, name='voice_input'),
    path('voice-api/', views.voice_api, name='voice_api'),
    path('summarize/', views.summarize, name='summarize'),
    
    # ✅ This name must match {% url 'upload_syllabus' %}
    path('upload/', views.upload_syllabus, name='upload_syllabus'),

    # ✅ quiz_generator handles both upload + quiz generation
    path('quiz-generator/', views.quiz_generator, name='quiz_generator'),
]