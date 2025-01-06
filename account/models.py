from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from  django.db.models.signals import post_save
import re
from django.core.exceptions import ValidationError

class GenderChoices(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    NONE = 'None'

class ExperienceChoices(models.TextChoices):
    FRESH = 'Fresh'
    JUNIOR = 'Junior'
    INTEMEDIATE = 'Intermediate'
    SENIOR = 'Senior'
    LEAD = 'Lead'
    MANAGER = 'Manager'

    

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/', default='profile_pic/default.jpg')
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=7, default=GenderChoices.NONE, blank=True, choices=GenderChoices.choices)
    phone_number = models.CharField(max_length=11, default='', blank=True)
    experience_level = models.CharField(max_length=20, default=ExperienceChoices.FRESH, blank=True, choices=ExperienceChoices.choices)

    address = models.CharField(max_length= 400, default= "", blank=True,)
    password_reset_otp = models.CharField(max_length=6, default="", blank=True)
    password_reset_expire = models.DateTimeField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.phone_number:
            if not re.match(r'^\d+$', self.phone_number):
                raise ValidationError("Phone Number must contain only digits.")

            if len(self.phone_number) != 11:
                raise ValidationError("Phone number must be exactly 11 digits.")

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)