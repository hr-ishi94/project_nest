# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

# class Profile(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     phone_number= models.CharField(max_length=10,blank=True)
#     otp=models.IntegerField()


from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserOTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timme_st = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    




