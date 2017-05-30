from django.contrib import admin
from .models import Person, camping_results, ApiParameters, Technologies, Demos, SuperHeroFight


# Register your models here.

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'marital', 'age', 'job')


@admin.register(camping_results)
class camping_resultsAdmin(admin.ModelAdmin):
    list_display = ('person', 'product', 'prediction')


@admin.register(ApiParameters)
class api_paramsAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'api_id', 'username')

@admin.register(Technologies)
class TechnologiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Demos)
class DemosAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(SuperHeroFight)
class SuperHeroFightAdmin(admin.ModelAdmin):
    list_display = ('SuperHeroOne', 'SuperHeroTwo')
