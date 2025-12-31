from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    pages = models.IntegerField()
    age_range = models.CharField(max_length=50, blank=True, null=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    language = models.CharField(max_length=10, default="en")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    cover_image = models.ImageField(upload_to="covers/", null=True, blank=True)
    # Using content_url instead of FileField as per requested Schema "content_url TEXT"
    content_url = models.URLField(max_length=500, help_text="Link to Canva PDF or hosted content")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "books"

    def __str__(self):
        return self.title

class UserLibrary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    access_granted = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_library"
        verbose_name_plural = "User Libraries"

    def __str__(self):
        return f"{self.user} - {self.book}"
