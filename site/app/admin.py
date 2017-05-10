from django.contrib import admin
from .models import Person, camping_results, api_params


# Register your models here.

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'marital', 'age', 'job')


@admin.register(camping_results)
class camping_resultsAdmin(admin.ModelAdmin):
    list_display = ('person', 'product', 'prediction')


@admin.register(api_params)
class api_paramsAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'api_id', 'username')