from django.contrib import admin
from .models import Student, Complaint, Visitor, Penalty

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostel', 'room')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved',)
    search_fields = ('student__user__username', 'subject')
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display =  ['student', 'name', 'visit_time', 'relation', 'purpose']

@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('student', 'reason', 'amount', 'date_issued')
