from django.views.generic import ListView

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "./books/book-list.html"
    paginate_by = 5
