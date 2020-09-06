from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver 

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    full_name = models.CharField(max_length=100, blank=True)

    bio = models.TextField(max_length=500, blank=True) 
    location = models.CharField(max_length=30, blank=True) 

    image = models.ImageField(upload_to='profile_picture', default='default.jpg') 

    caretaker = models.BooleanField(default=False)

    phone_number_verified = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs): 
#     instance.profile.save() 

class Connect(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="connect_user")
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="connect_other_user")
    connect = models.BooleanField(default=False)
    connected = models.BooleanField(default=False)

class VerifyInfo(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verifyinfo")
    
    email = models.EmailField(null=True) 
    phone_number = models.IntegerField(null=True) 
    country_code = models.IntegerField(null=True) 

    authy_id = models.IntegerField(null=True)
    profile_complete = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_verification_info(sender, instance, created, **kwargs): 
    if created: 
        VerifyInfo.objects.create(user=instance).save()

# @receiver(post_save, sender=User)
# def save_verification_info(sender, instance, created, **kwargs): 
#     instance.verifyinfo.save() 
