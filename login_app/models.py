from __future__ import unicode_literals
from django.db import models
import re
from django.contrib import messages
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def vablator(self, data):
        errors = {}
        if len(data['first_name']) < 1:
            errors['first_name'] = "First name cannot be blank!"
        if len(data['last_name']) < 1:
            errors['last_name'] = "Last name cannot be blank!"
        if len(data['email']) < 8:
            errors['email'] = "Email needs to be longer!"
        if not EMAIL_REGEX.match(data['email']):
            errors['regex'] = "Invalid email address!"
        email_check = self.filter(email= data['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if data['password'] != data['confirm_pw']:
            errors['password'] = "Passwords do not match."
        return errors

    def authenticate(self, email, password):
        user = None
        try:
            user = User.objects.get(email = email)
        except:
            return False
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, data):
        pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password = pw,
        )

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts')

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="user_comments", on_delete=models.CASCADE)
