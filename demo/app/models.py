from __future__ import unicode_literals
from django.db import models


class Technologies(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Demos(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    technologies = models.ManyToManyField(Technologies)
    path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


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
        ('ex', 'Executive'),
        ('ho', 'Hospitality'),
        ('ot', 'Other'),
        ('pr', 'Professional'),
        ('re', 'Retail'),
        ('rr', 'Retired'),
        ('sa', 'Sales'),
        ('st', 'Student'),
        ('tr', 'Trades'),
    )

    age_c = []
    for a in range(20, 70, 5):
        age_c.append([a, a])

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_c)
    marital = models.CharField(max_length=1, choices=marital_c)
    age = models.IntegerField(choices=age_c)
    job = models.CharField(max_length=2, choices=job_c)

    def __str__(self):
        return self.name


class camping_results(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    rawprediction = models.TextField()
    product = models.CharField(max_length=30)
    prediction = models.FloatField()


class ApiParameters(models.Model):
    api_name = models.CharField(max_length=30, default='')
    api_id = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=255, null=True)
    service_path = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    endpoint = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True)


class SuperHero(models.Model):
    heroid = models.IntegerField()
    hero = models.CharField(max_length=100)
    Role = models.CharField(max_length=100)
    Efficienyv = models.DecimalField(decimal_places=2, max_digits=5)
    Mitigationv = models.DecimalField(decimal_places=2, max_digits=5)
    Suportv = models.DecimalField(decimal_places=2, max_digits=5)
    Ultimates = models.DecimalField(decimal_places=2, max_digits=5)
    Scalingv = models.DecimalField(decimal_places=2, max_digits=5)
    Productionv = models.DecimalField(decimal_places=2, max_digits=5)
    Depthv = models.DecimalField(decimal_places=2, max_digits=5)
    Funv = models.DecimalField(decimal_places=2, max_digits=5)
    DE = models.DecimalField(decimal_places=2, max_digits=5)
    Fights = models.DecimalField(decimal_places=2, max_digits=5)

class SuperHeroFight(models.Model):
    heroes = [[0, 'Scarlet Witch'], [1, 'Jean Grey'], [2, 'Dr. Doom'], [3, 'Magik'], [4, 'Vision'],
              [5, 'Black Panther'],
              [6, 'Capt. America'], [7, 'Doctor Strange'], [8, 'Silver Surfer'], [9, 'Cable'], [10, 'Thor'],
              [11, 'Iceman'], [12, 'Loki'], [13, 'War Machine'], [14, 'Kitty Pryde'], [15, 'Invisible Woman'],
              [16, 'Rocket Raccoon'], [17, 'Punisher'], [18, 'Spiderman'], [19, 'Rogue'], [20, 'Thing'], [21, 'Venom'],
              [22, 'Blade'], [23, 'Cyclops'], [24, 'Nova'], [25, 'She Hulk'], [26, 'Iron Man'], [27, 'Ms. Marvel'],
              [28, 'Gambit'], [29, 'Antman'], [30, 'Taskmaster'], [31, 'Hulk'], [32, 'Mr. Fantastic'],
              [33, 'Moon Knight'], [34, 'Psylocke'], [35, 'Winter Soldier'], [36, 'Ghost Rider'], [37, 'Juggernaut'],
              [38, 'Hawkeye'], [39, 'Human Torch'], [40, 'Iron Fist'], [41, 'Black Widow'], [42, 'Storm'],
              [43, 'Emma Frost'], [44, 'Wolverine'], [45, 'Luke Cage'], [46, 'Daredevil'], [47, 'X23'], [48, 'Magneto'],
              [49, 'Nightcrawler'], [50, 'Colossus'], [51, 'Starlord'], [52, 'Squirrel Girl'], [53, 'Deadpool']]

    SuperHeroOne = models.IntegerField(name="SuperHeroOne", choices=heroes)
    heroone_score = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)
    SuperHeroTwo = models.IntegerField(name="SuperHeroTwo", choices=heroes)
    herotwo_score = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)

    def get_winner(self):
        if self.heroone_score > self.herotwo_score:
            return self.SuperHeroOne
        elif self.heroone_score < self.herotwo_score:
            return self.SuperHeroTwo
        elif self.heroone_score == self.herotwo_score:
            return "tie"
        else:
            return "na"

    winner = property(get_winner)

    def get_queryset(self):
        """Overrides the models.Manager method"""
        qs = super(SuperHeroFight, self).get_queryset().annotate(winner=winner)
        return qs
