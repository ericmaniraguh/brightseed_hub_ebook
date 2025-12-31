from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, VerifyOTPSerializer, UserSerializer
from .models import OTP
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Generate OTP
        code = str(random.randint(100000, 999999))
        expiry = timezone.now() + timedelta(minutes=10)
        OTP.objects.create(user=user, code=code, expires_at=expiry)
        
        # In production, send via Email/SMS
        print(f"DEBUG: OTP for {user.email} is {code}") 

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            otp_record = OTP.objects.filter(user=user, code=code, is_used=False).first()
            
            if otp_record and otp_record.expires_at > timezone.now():
                otp_record.is_used = True
                otp_record.save()
                
                user.is_verified = True
                user.is_active = True
                user.save()
                
                return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
