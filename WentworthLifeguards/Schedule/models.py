from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Employees(models.Model):
    print(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    Availability = models.ManyToManyField('Shifts', blank=True, default=None)
    PhoneNo = models.IntegerField(validators=[MinValueValidator(7000000000),MaxValueValidator(7999999999)])
    isManager = models.BooleanField(default=False)


class Shifts(models.Model):
    Start = models.DateTimeField()
    End = models.DateTimeField()
    Employees = models.OneToOneField('Employees', blank=True, default=None, null=True, on_delete=models.SET_DEFAULT)
    ShiftNotes = models.TextField(blank=True)
    CoverRequest = None
    Active = models.BooleanField(default=False)


