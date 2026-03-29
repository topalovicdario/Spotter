from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    CLIENT = 'CLIENT'
    TRAINER = 'TRAINER'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (TRAINER, 'Trainer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    def is_trainer(self):
        return self.role == self.TRAINER

    def is_client(self):
        return self.role == self.CLIENT

class Portfolio(models.Model):
    trainer = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={'role': User.TRAINER},
        related_name='portfolio'
    )
    profession = models.CharField()
    bio = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True, null=True)


class Card(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('PENDING', 'Pending'),
        ('CLOSED', 'Closed'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.CLIENT}
    )
    problem = models.TextField()
    goal = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)

class Response(models.Model):
    STATUS_CHOICES = [
        ('ACCEPTED', 'Accepted'),
        ('PENDING', 'Pending'),
        ('DECLINED', 'Declined'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.TRAINER}
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="response",
    )
    pitch = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    planIsCreated=models.BooleanField(default=False)

class Plan(models.Model):
    response=models.OneToOneField(Response,on_delete=models.CASCADE,related_name='plan', null=True,blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_plans')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_plans')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration= models.IntegerField(help_text="Duration in days")
    isActive=models.BooleanField(default=True)

class DailyPlan(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Exercise(models.Model):
    dailyPlan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    sets = models.IntegerField()
    reps = models.IntegerField()


class Meal(models.Model):
    MEAL_TYPE = [
    ('BREAKFAST', 'Breakfast'),
    ('BRUNCH', 'Brunch'),
    ('LUNCH', 'Lunch'),
    ('SNACK', 'Snack'),
    ('DINNER', 'Dinner'),
    ('SUPPER', 'Supper'),
    ('DESSERT', 'Dessert'),
    ('DRINK', 'Drink'),
    ]

    mealType= models.CharField(
        max_length=20,
        choices=MEAL_TYPE,
        default='LUNCH'
    )
    dailyPlan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    image_url = models.URLField(blank=True, null=True)
    calories = models.IntegerField()

class ProgressComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rejection(models.Model):
    plan= models.ForeignKey(Plan, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
