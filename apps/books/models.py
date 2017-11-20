from __future__ import unicode_literals
from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "First name should be more than 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be more than 2 characters"    
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        if postData['password'] != postData['conf_pw']:
            errors['password_confirm']= "Password and confirm pw must match"
        if len(postData['password']) < 8:
            errors['password'] = "Password shoud be more than 8 characters."
        if self.filter(email = postData['email']):
            errors['email_exist'] = "The email you entered already exists."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class Author(models.Model):
  name = models.CharField(max_length=255)

class Book(models.Model):
  title = models.CharField(max_length=255)
  author = models.ForeignKey(Author, related_name = "book")

class Review(models.Model):
  body = models.TextField()
  rating = models.IntegerField()
  created_at = models.DateField(auto_now_add = 	True)
  user = models.ForeignKey(User, related_name = "review")
  book = models.ForeignKey(Book, related_name = "review")
