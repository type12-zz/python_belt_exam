from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors ={}
        
        #adds keys and values to error dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should have at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should have at least 2 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should at least have 8 characters"
        if (postData['password'] != postData['confirm_password']):
            errors['confirm_password'] = "Passwords do not match!!"
        return errors

    def login_validator(self, postData):
        errors={}    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should at least have 8 characters"
        return errors

class Quote_Manager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author should at least have 3 characters"
        if len(postData['quote_bar']) < 10:
            errors['quote_bar'] = "Quotes should at least have 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    user_thought = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    liked_quote = models.ManyToManyField(User, related_name='users_who_liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Quote_Manager()