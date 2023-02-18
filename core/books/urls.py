from django.urls import path, include
from .views import BookListView

urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("api/v1/", include("books.api.v1.urls")),
]
