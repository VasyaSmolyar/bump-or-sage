from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    img_url = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now),
    user = models.ForeignKey(User,on_delete = models.CASCADE)

class Vote(models.Model):
    img = models.ForeignKey(Image,on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
