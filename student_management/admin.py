from django.contrib import admin
from .models import Student, Attendance, AcademicRecord, StudentDocument

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department')  # adjust to your model fields
    search_fields = ('user__username', 'roll_number', 'department')
    list_filter = ('department',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__user__username',)

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'subject', 'marks_obtained', 'max_marks')
    search_fields = ('student__user__username', 'subject')

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'uploaded_at')
    search_fields = ('student__user__username', 'title')


# admin.site.register(Student)
# admin.site.register(Attendance)