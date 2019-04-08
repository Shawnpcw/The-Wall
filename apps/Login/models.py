from django.core.validators import validate_slug, validate_email
from django.db import models
import bcrypt
class UserManager(models.Manager):
    def basic_validator(self, postData):
        result = {}
        errors = []
        print(postData['email'])
        Current_email = User.objects.filter(email=postData['email'])
        print(Current_email)
        if len(postData['first_name']) <3:
            errors.append('First name should be at least 4 charaters!')
        if any(i.isdigit() for i in postData['first_name']):
            errors.append('First name should be only letters!')
        if len(postData['last_name']) <3:
            errors.append('Last name should be at least 4 charaters!')
        if any(i.isdigit() for i in postData['last_name']):
            errors.append('Last name should be only letters!')
        if len(postData['email']) <3:
            errors.append('Email should be at least 4 charaters!')
        if ('@' not in postData['email']):
            errors.append('Email needs a "@"!')
        if len(Current_email)>0:
            errors.append('Email already exists!')
        if len(postData['password']) <7:
            errors.append('Password should be at least 8 charaters!')
        if postData['password'] != postData['pwcheck']:
            errors.append('Passwords dont match!')
        print(errors)

        if len(errors) ==0:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user =User.objects.create(first_name=postData['first_name'],last_name = postData['last_name'], email = postData['email'], pw_hash = hashed_pw.decode())
            result['user_id'] = new_user.id
        else:
            result['errors'] = errors
        return result
    def login_validator(self, postData):
        result = {}
        errors = []
        user = User.objects.filter(email=postData['email'])
        print('*'*50)
        if len(user) ==1:
            pw_hash = user[0].pw_hash
            print(pw_hash)
            if bcrypt.checkpw(postData['password'].encode(),pw_hash.encode()):
                print("password match")
                result['user_id'] = user[0].id
            else:
                print("failed password") 
                errors.append('Email or Password Incorrect')
                result['errors'] = errors
        else:
            errors.append('Email or Password Incorrect')
            print('failed retreving email') 
            result['errors'] = errors
        return result
class User(models.Model):
    first_name = models.CharField(max_length =255)
    last_name = models.CharField(max_length =255)
    email = models.CharField(max_length =255,validators=[validate_email])
    pw_hash = models.CharField(max_length =255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    message_uploader = models.ForeignKey(User, related_name='uploaded_message',on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    comment_uploader = models.ForeignKey(User, related_name='uploaded_comment',on_delete=models.CASCADE)
    comment_message = models.ForeignKey(Message, related_name='message_comment',on_delete=models.CASCADE)
