from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Purchase
from .serializers import PurchaseSerializer
from apps.books.models import Book
import uuid

class PurchaseListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users see only their own purchases
        return Purchase.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Generate a transaction ID mainly for the pending state
        transaction_id = str(uuid.uuid4())
        serializer.save(user=self.request.user, transaction_id=transaction_id)
