from django.db import models
import re, bcrypt
from datetime import datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if len(postData['fname']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['emailpattern'] = "Invalid email address" 
        user = User.objects.filter(email=postData['email'])
        if user:
            register_user = user[0]
            errors['existid'] ="Eamil Address is already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Password and confirm PW must match"
        return errors

    def loginVal(self, postData):
        errors= {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['wrongpw'] ="Password does not match"
        else:
            errors['unregistered'] = "Username not registered. Try agian"
        return errors

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    # picture = models.ImageField(upload_to="forums", default='forums/default.jpg', blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10 ,decimal_places=2)
    image = models.ImageField(upload_to="forums", default=None, blank=True, null=True)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class List(models.Model):
    buyer = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    obj = models.ForeignKey(Item, related_name="buyers", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Review(models.Model):
    creator = models.ForeignKey(User, related_name="userreviews", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="reviews", on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.IntegerField()
    like = models.ManyToManyField(User, related_name="like_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

