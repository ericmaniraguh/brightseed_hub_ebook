from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=255, default="Unknown")
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, default='USER')
    is_verified = models.BooleanField(default=False)
    # created_at is handled by date_joined in AbstractUser, but we can add an alias property or field if strictly needed.
    # We will stick to date_joined for Django compatibility unless strictly necessary.




    def __str__(self):
        return self.username

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "OTP Code"
        db_table = "otp_codes"

    def __str__(self):
        return f"{self.user.username} - {self.code}"
