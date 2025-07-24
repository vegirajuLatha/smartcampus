# library/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_dashboard, name='library-dashboard'),  # Home/dashboard

    # Book Management
    path('books/', views.book_inventory, name='book-inventory'),
    path('books/add/', views.add_book, name='add-book'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit-book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete-book'),
    path('books/borrow/<int:pk>/', views.borrow_book, name='borrow-book'),
    path('books/return/<int:book_id>/', views.return_book, name='return-book'),
    path('books/list/', views.book_list, name='book_list'),  # renamed to avoid conflict

    # Borrow Logs
    path('logs/', views.borrow_logs, name='borrow-logs'),
    path('logs/all/', views.borrow_log_view, name='all-borrow-logs'),

    # Penalties
    path('penalties/', views.penalty_tracker, name='penalty-tracker'),
    path('admin/penalties/', views.all_penalties_view, name='admin-penalties'),

    # Book Recommender
    path('recommender/', views.book_recommender, name='book_recommender'),

    # Borrow/Return
    path('borrow-return/', views.borrow_return_page, name='borrow_return_page'),
    path('book-recommender/', views.book_recommender, name='book-recommender'),
    

]