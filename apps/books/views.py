from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'language']
    search_fields = ['title', 'description']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
