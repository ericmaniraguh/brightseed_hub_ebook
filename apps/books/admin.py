from django.contrib import admin
from .models import Book, Category, UserLibrary

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'language', 'is_active')
    list_filter = ('category', 'language', 'is_active')
    search_fields = ('title', 'description')

@admin.register(UserLibrary)
class UserLibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'access_granted', 'added_at')
    list_filter = ('access_granted',)
