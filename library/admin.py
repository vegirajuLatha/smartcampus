from django.contrib import admin
from .models import Book, BorrowLog, BorrowedBook  # ✅ No Penalty here

admin.site.register(Book)
admin.site.register(BorrowLog)
admin.site.register(BorrowedBook)