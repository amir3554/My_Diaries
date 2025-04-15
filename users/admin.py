from django.contrib import admin
from . import models

@admin.register(models.CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 20
