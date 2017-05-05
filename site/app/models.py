from __future__ import unicode_literals
from django.db import models

class Person(models.Model):
    gender_c = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    marital_c = (
        ('M', 'Married'),
        ('S', 'Single'),
        ('O', 'Other')
    )

    job_c = (
        ('ex','Executive'),
        ('ho', 'Hospitality'),
        ('ot', 'Other'),
        ('pr', 'Professional'),
        ('re', 'Retail'),
        ('rr', 'Retired'),
        ('sa', 'Sales'),
        ('st', 'Student'),
        ('tr', 'Trades'),
    )


    name_text = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_c)
    marital = models.CharField(max_length=1, choices=marital_c)
    age = models.IntegerField()
    job = models.CharField(max_length=2, choices=job_c)

class results(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
