
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, filters

from ...models import Book, Author, Category
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrReadOnlyDetails


class CustomSearchFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value is not None:
            lookup = f"{self.field_name}__icontains"
            return qs.filter(**{lookup: value})
        return qs


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class BookList(ListCreateAPIView):
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "pk"
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "title": ["icontains"],
        "description": ["icontains"],
        "authors": ["icontains"],
        "categories": ["icontains"],
    }

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset


class BookDetails(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.filter()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "pk"
    permission_classes = [IsAdminOrReadOnly]


class AuthorDetails(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "pk"
    permission_classes = [IsAdminOrReadOnlyDetails]


class AuthorsList(ListCreateAPIView):
    serializer_class = AuthorSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"name": ["icontains"]}

    def get_queryset(self):
        queryset = Author.objects.all()
        return queryset


class CategoriesList(ListCreateAPIView):
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"name": ["icontains"]}

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnlyDetails]
