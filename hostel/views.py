from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .models import Complaint, Penalty, Student, Visitor
from .forms import ComplaintForm,VisitorForm
from django import forms

# ==========================================================
# 📌 DASHBOARD REDIRECT BASED ON ROLE
# ==========================================================

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('hostel-admin-dashboard')
    else:
        return redirect('student-dashboard')

# ==========================================================
# 👮 ADMIN DASHBOARD VIEW
# ==========================================================

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'hostel/admin_dashboard.html')

# ==========================================================
# 🧑‍🎓 STUDENT DASHBOARD VIEW
# ==========================================================

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'hostel/not_student.html')

    complaints = Complaint.objects.filter(student=student)
    penalties = Penalty.objects.filter(student=student)
    visitors = Visitor.objects.filter(student=student)

    context = {
        'student': student,
        'complaints': complaints,
        'penalties': penalties,
        'visitors': visitors,
    }
    return render(request, 'hostel/student_dashboard.html', context)

# ==========================================================
# ✉ SUBMIT COMPLAINT (STUDENT)
# ==========================================================
from hostel.models import Complaint, Student  # ensure this is imported

@login_required
def submit_complaint(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'hostel/not_student.html')

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = student
            complaint.save()
            messages.success(request, "✅ Complaint submitted successfully.")
            form = ComplaintForm()  # reset form
    else:
        form = ComplaintForm()

    return render(request, 'hostel/submit_complaint.html', {'form': form})
@login_required
def view_penalties(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'hostel/not_student.html')

    penalties = Penalty.objects.filter(student=student)
    return render(request, 'hostel/view_penalties.html', {'penalties': penalties})

# ==========================================================
# 📑 VIEW COMPLAINTS (ADMIN)
# ==========================================================

@user_passes_test(lambda u: u.is_superuser)
def view_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'hostel/view_complaints.html', {'complaints': complaints})

# ==========================================================
# ➕ ADD PENALTY (ADMIN)
# ==========================================================

class PenaltyForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['student', 'reason', 'amount']
from django.contrib import messages
@login_required
def add_penalty(request):
    if request.method == 'POST':
        form = PenaltyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Penalty assigned successfully.")
            return redirect('view_penalties')  # ensure this URL name exists
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = PenaltyForm()

    return render(request, 'hostel/add_penalty.html', {'form': form})
# ==========================================================
# 🧾 ADD VISITOR (ADMIN)
# ==========================================================
# class VisitorForm(forms.ModelForm):
#     class Meta:
#         model = Visitor
#         fields = ['student', 'name', 'relation', 'purpose', 'visit_time']

@login_required
def add_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Visitor added successfully.")
            return redirect('view_visitors')  # update this if your success page is different
    else:
        form = VisitorForm()
    return render(request, 'hostel/add_visitor.html', {'form': form})
# ==========================================================
# 👨‍🎓 VIEW STUDENTS (ADMIN)
# ==========================================================

@user_passes_test(lambda u: u.is_superuser)
def view_students(request):
    students = Student.objects.all()
    return render(request, 'hostel/view_students.html', {'students': students})

@login_required
def hostel_dashboard(request):
    return render(request, 'hostel/dashboard.html')

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('hostel-admin-dashboard')
    else:
        return redirect('student-dashboard')
    
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'hostel/admin_dashboard.html')

from .models import Visitor, Student

@login_required
def view_visitors(request):
    user = request.user

    if hasattr(user, 'student_profile'):
        # Student: show only their visitors
        student = user.student_profile
        visitors = Visitor.objects.filter(student=student)
    else:
        # Admin: show all visitors
        visitors = Visitor.objects.all()

    return render(request, 'hostel/view_visitors.html', {'visitors': visitors})