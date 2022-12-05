from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer_Data(models.Model):
    username=models.CharField(max_length=90)
    email=models.EmailField()
    pass1=models.CharField(max_length=10)
    pass2=models.CharField(max_length=10)
    def __str__(self):
        return self.username

class Profile(models.Model):
    username=models.CharField(max_length=50)
    user=models.OneToOneField( User, on_delete=models.CASCADE)
    email_token=models.CharField( max_length=200)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.user.username 
