from django.db import models

# Create your models here.

class Image(models.Model):
    path = models.TextField(null = True)
    content = models.BinaryField(null = True)
    date = models.DateTimeField(auto_now_add = True)