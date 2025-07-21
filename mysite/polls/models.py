from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
   


class VoterManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Voter(AbstractBaseUser):
   username = models.CharField(max_length=30, unique=True, null=True, blank=True)
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   email = models.EmailField(verbose_name="email address",max_length=255, unique=True,)
   date_of_birth = models.DateField(null=True, blank=True)
   is_active = models.BooleanField(default=True)
   is_admin = models.BooleanField(default=False)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

   objects = VoterManager()

   
   def __str__(self):
        return self.username or self.email
   
   def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
   
   def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
   
   @property
   def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

   
    
class User_Question(models.Model):
    user = models.ForeignKey(Voter, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

