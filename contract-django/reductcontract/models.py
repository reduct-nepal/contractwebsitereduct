from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from PIL import Image
import datetime


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    images = models.ImageField(default='myprofile.png', upload_to='images/')

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()
        img=Image.open(self.images.path)
        if img.height >300 or img.width >300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.images.path)

class contractor(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    role=models.CharField(max_length=20)
    contract_duration=models.IntegerField()
    start_date=models.DateField()
    finish_date=models.DateField()
    on_board=models.DateField(default=datetime.date.today)
    clause=models.CharField(null=True,max_length=250)
    address=models.CharField(max_length=100)
    email=models.EmailField()
    phone_number=models.IntegerField()
    status=models.TextField(null=True)


    class Meta:
        ordering=['finish_date']

    def __str__(self):
        return self.user.username


# models.py

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
