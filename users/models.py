from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import pyotp
#from courses.models import Course
#from django.contrib.auth import get_user_model

#User = get_user_model()


class UserManager(BaseUserManager):
    def create_user(self, email, password = None, role = "student" , **extra_fields):
        if not email:
            raise ValueError("Email is required") 
        email = self.normalize_email(email)
        user = self.model(email = email,role =role ,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password,**extra_fields)
    



class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student',"Student"),
        ("instructor","Instructor"),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length = 30 , blank=True)
    last_name = models.CharField(max_length = 30, blank=True)
    profile_picture = models.ImageField(upload_to= "profiles/", blank =True , null=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_2fa_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    #course = models.ForeignKey("courses.Course" , on_delete=models.CASCADE , name= "user_courses")



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['role']
        
    objects = UserManager()


    def save(self, *args,**kwargs):
        if self.is_2fa_enabled and not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
        super().save(*args,**kwargs)

    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(name=self.email, issuer_name="OnlineCoursePlatform")        


    def __str__(self):
        return f"{self.email} ({self.role})"
    
    
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(null = True, blank = True)
    user_agent = models.TextField(null = True , blank =True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} at {self.timestamp}"
    


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null= True , blank= True)
    user_agent = models.TextField(null = True , blank=True)    


    def __str__(self):
        return f"{self.user.email} logged in at {self.timestamp}"
    




class Notification(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Notifications")
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"] 