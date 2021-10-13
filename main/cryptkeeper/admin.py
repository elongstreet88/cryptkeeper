from django.contrib import admin
from .models import *

@admin.register(Transaction)
class HeroAdmin(admin.ModelAdmin):
    ...
    readonly_fields = ["user"]
