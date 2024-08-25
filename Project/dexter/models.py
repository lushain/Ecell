from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Invention(models.Model):
#     name  = models.CharField(max_length= 100)
#     img  = models.ImageField(upload_to= 'pics')
#     desc  = models.TextField()

#     # def __str__(self):
#     #     return self.name


# class UserInvention(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product_id = models.IntegerField()

#     # def __str__(self):
#     #     return self.user


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2500)
    img = models.ImageField(upload_to='pics')

