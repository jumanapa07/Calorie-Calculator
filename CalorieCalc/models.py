# myapp/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)

    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default="O")
    objects = CustomUserManager()

class Food(models.Model):
    food_name = models.CharField(max_length=200)
    serving_size = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    calories = models.IntegerField(default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
    protein = models.DecimalField(max_digits=7, decimal_places=2)
    fiber = models.DecimalField(max_digits=7, decimal_places=2)
    sugar = models.DecimalField(max_digits=7, decimal_places=2)
    cholestrol = models.DecimalField(max_digits=7, decimal_places=2)
    # category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='food_category')

    def __str__(self):
        return f'{self.food_name} - calories: {self.calories}'
    
class FoodLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category=models.CharField(max_length=100,default='')
    food_consumed = models.TextField(max_length=100,default='')
    quantity = models.DecimalField(max_digits=7, decimal_places=3,blank=True, null=True,default=1)
    unit = models.TextField(blank=True, null=True,default='')
    serving_weight = models.TextField(blank=True, null=True,default='')
    calories=models.DecimalField(max_digits=7, decimal_places=3)
    # date_logged=models.DateField()
    created_at = models.DateField(auto_now_add=True)



class ExerciseLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.FloatField()
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

class Weight(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name='weights')
    weight=models.PositiveIntegerField()
    date=models.DateField()


class Plan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name='weight_plan')
    created_at = models.DateField(auto_now_add=True)
    current_weight=models.PositiveIntegerField()
    target_weight=models.PositiveIntegerField()
    target_duration=models.PositiveIntegerField()
    target_rate=models.FloatField()
    calorie_needed=models.FloatField()
