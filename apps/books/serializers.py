from rest_framework import serializers
from .models import Book, Category, UserLibrary

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    has_access = serializers.SerializerMethodField()
    content_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'pages', 'age_range', 'category', 
                  'language', 'price', 'cover_image', 'has_access', 'content_url', 'created_at']

    def get_has_access(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            # Check if user has access via UserLibrary
            return UserLibrary.objects.filter(user=user, book=obj, access_granted=True).exists()
        return False

    def get_content_url(self, obj):
        if self.get_has_access(obj):
            return obj.content_url
        return None  # Hide content URL if not purchased
