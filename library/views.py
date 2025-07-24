from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Book, BorrowLog, BorrowedBook, Penalty
from .forms import BookForm
import random
from datetime import timedelta
from django.utils.timezone import now

# ========== Utility Check ==========
def is_admin(user):
    return user.is_staff

# ========== Dashboard ==========
@login_required
def library_dashboard(request):
    return render(request, 'library/dashboard.html')

# ========== Book Inventory with Search, Filter, Pagination ==========
@login_required
def book_inventory(request):
    query = request.GET.get('q', '')
    filter_category = request.GET.get('category', '')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    if filter_category:
        books = books.filter(category__icontains=filter_category)

    books = books.order_by('title')
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/book_inventory.html', {
        'books': page_obj,
        'query': query,
        'filter_category': filter_category
    })

# ========== Book Add/Edit/Delete ==========
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('book-inventory')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Add'})

@user_passes_test(is_admin)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, "Book updated successfully.")
        return redirect('book-inventory')
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Edit'})

@user_passes_test(is_admin)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, "Book deleted.")
    return redirect('book-inventory')

# ========== Penalty Check Logic ==========
def check_and_issue_penalty(user, book):
    borrowed = BorrowedBook.objects.filter(
        user=user,
        book=book,
        returned_date__isnull=True
    ).first()

    if borrowed and (timezone.now().date() - borrowed.borrowed_date.date() > timedelta(days=14)):
        Penalty.objects.create(
            user=user,
            book=book,
            amount=50,
            reason="Late return (more than 14 days)",
            issued_on=timezone.now().date()
        )

# ========== Borrow/Return Book ==========
@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.is_available:
        book.is_available = False
        book.save()

        BorrowLog.objects.create(
            user=request.user,
            book=book,
            action='borrowed'
        )

        BorrowedBook.objects.create(
            user=request.user,
            book=book,
            borrowed_date=timezone.now()
        )

        messages.success(request, f"You have borrowed '{book.title}'.")
    else:
        messages.error(request, f"'{book.title}' is not available.")
    return redirect('book-inventory')

@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrowed = BorrowedBook.objects.filter(
        user=request.user,
        book=book,
        returned_date__isnull=True
    ).first()

    if borrowed:
        borrowed.returned_date = timezone.now()
        borrowed.save()

        book.is_available = True
        book.save()

        # ✅ Check and issue penalty
        check_and_issue_penalty(request.user, book)

        BorrowLog.objects.create(
            user=request.user,
            book=book,
            action='returned'
        )

        messages.success(request, f"You have returned '{book.title}'.")
    else:
        messages.warning(request, f"No active borrow record found for '{book.title}'.")

    return redirect('book-inventory')

# ========== Borrow Logs ==========
@login_required
def borrow_logs(request):
    logs = BorrowLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'library/borrow_logs.html', {'logs': logs})

@user_passes_test(is_admin)
def borrow_log_view(request):
    logs = BorrowLog.objects.all().order_by('-timestamp')
    return render(request, 'library/borrow_logs.html', {'logs': logs})

# ========== Penalty Tracker ==========
@login_required
def penalty_tracker(request):
    borrowed_books = BorrowedBook.objects.filter(
        user=request.user,
        returned_date__isnull=True
    )

    for record in borrowed_books:
        delta_days = (record.due_date - now().date()).days
        record.remaining_days = delta_days  # can be negative
        record.abs_remaining_days = abs(delta_days)  # always positive
        record.penalty_display = record.penalty_amount  # use this in template

    return render(request, 'library/penalty_tracker.html', {
        'borrowed_books': borrowed_books
    })

@user_passes_test(is_admin)
def all_penalties_view(request):
    penalties = Penalty.objects.all().order_by('-issued_on')
    return render(request, 'library/penalty_admin_view.html', {'penalties': penalties})

# ========== Book List ==========
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def book_recommender(request):
    genre = request.GET.get('genre', '').strip()

    if genre:
        recommended_books = Book.objects.filter(category__icontains=genre).order_by('?')[:5]
        context_msg = f"Recommendations for genre: '{genre}'"
    else:
        borrowed_categories = BorrowedBook.objects.filter(user=request.user) \
            .values_list('book__category', flat=True).distinct()

        borrowed_books = BorrowedBook.objects.filter(user=request.user) \
            .values_list('book__id', flat=True)

        recommended_books = Book.objects.filter(
            category__in=borrowed_categories
        ).exclude(
            id__in=borrowed_books
        ).order_by('?')[:5]

        if not recommended_books.exists():
            recommended_books = Book.objects.exclude(id__in=borrowed_books).order_by('?')[:5]
        
        context_msg = "Recommended based on your borrowing history"

    return render(request, 'library/book_recommender.html', {
        'recommended_books': recommended_books,
        'context_msg': context_msg,
        'genre_input': genre,
    })

# ========== Borrow & Return Combined Page ==========
@login_required
def borrow_return_page(request):
    books = Book.objects.all()

    if request.method == "POST":
        book_id = request.POST.get("book_id")
        action = request.POST.get("action")
        book = get_object_or_404(Book, id=book_id)

        if action == "borrow":
            already_borrowed = BorrowedBook.objects.filter(
                user=request.user,
                book=book,
                returned_date__isnull=True
            ).exists()

            if not already_borrowed:
                BorrowedBook.objects.create(
                    user=request.user,
                    book=book,
                    borrowed_date=timezone.now()
                )
                book.is_available = False
                book.save()
                messages.success(request, f"You have borrowed '{book.title}'.")
            else:
                messages.warning(request, f"You have already borrowed '{book.title}'.")

        elif action == "return":
            borrowed = BorrowedBook.objects.filter(
                user=request.user,
                book=book,
                returned_date__isnull=True
            ).first()

            if borrowed:
                borrowed.returned_date = timezone.now()
                borrowed.save()
                book.is_available = True
                book.save()

                # ✅ Check and issue penalty here too
                check_and_issue_penalty(request.user, book)

                messages.success(request, f"You have returned '{book.title}'.")
            else:
                messages.warning(request, f"No active borrow record found for '{book.title}'.")

        return redirect('borrow_return_page')

    borrowed_books = BorrowedBook.objects.filter(
        user=request.user,
        returned_date__isnull=True
    )

    return render(request, 'library/borrow_return.html', {
        'books': books,
        'borrowed_books': borrowed_books,
    })