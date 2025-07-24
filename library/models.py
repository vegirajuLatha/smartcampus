from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, date

# ===============================
# ✅ Book Model
# ===============================
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="General")
    is_available = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)  # Optional

    def _str_(self):
        return self.title

# ===============================
# ✅ Borrow Log (Optional)
# ===============================
class BorrowLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} {self.action} {self.book.title}"

# ===============================
# ✅ Borrowed Book Model
# ===============================
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    def _str_(self):
        return f"{self.user.username} borrowed {self.book.title}"

    @property
    def due_date(self):
        return self.borrowed_date + timedelta(days=5)

    @property
    def is_overdue(self):
        today = date.today()
        if self.returned_date:
            return self.returned_date > self.due_date
        return today > self.due_date

    @property
    def penalty_amount(self):
        today = date.today()
        if self.returned_date:
            late_days = (self.returned_date - self.due_date).days
        else:
            late_days = (today - self.due_date).days
        return 100 * max(0, late_days)

# ===============================
# ✅ Penalty Model
# ===============================
class Penalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1) 
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    reason = models.CharField(max_length=255)
    issued_on = models.DateField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - ₹{self.amount} for '{self.book.title}'"