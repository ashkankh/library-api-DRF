from django.urls import path
from .views import (
    BookList,
    AuthorsList,
    AuthorDetails,
    BookDetails,
    CategoriesList,
    CategoryDetails,
)

urlpatterns = [
    path("book/", BookList.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetails.as_view(), name="book_details"),
    path("author/", AuthorsList.as_view(), name="author-list"),
    path("author/<int:pk>/", AuthorDetails.as_view(), name="author_details"),
    path("category/", CategoriesList.as_view(), name="category-list"),
    path("category/<int:pk>/", CategoryDetails.as_view(), name="category_details"),
]
