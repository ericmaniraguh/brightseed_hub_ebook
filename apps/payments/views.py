from rest_framework import views, status, permissions
from rest_framework.response import Response
from apps.orders.models import Purchase
from apps.books.models import UserLibrary, Book

class MockPaymentProcessView(views.APIView):
    """
    Simulates a payment gateway callback or process execution.
    In real life, this would be a webhook from Stripe/PayPal.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        payment_token = request.data.get('payment_token') # Simulation token

        if not order_id:
            return Response({"error": "Order ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase = Purchase.objects.get(id=order_id, user=request.user)
        except Purchase.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if purchase.payment_status == 'SUCCESS':
            return Response({"message": "Order already paid"}, status=status.HTTP_200_OK)

        # SIMULATE PAYMENT SUCCESS
        # In a real app, verify 'payment_token' with Stripe/PayPal here.
        
        purchase.payment_status = 'SUCCESS'
        purchase.save()

        # Grant access to the book
        UserLibrary.objects.get_or_create(
            user=request.user,
            book=purchase.book,
            defaults={'access_granted': True}
        )

        return Response({
            "message": "Payment successful",
            "status": "SUCCESS",
            "book_title": purchase.book.title
        })
