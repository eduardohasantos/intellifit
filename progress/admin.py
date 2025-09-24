from django.contrib import admin
from .models import ProgressEntry

@admin.register(ProgressEntry)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'water_ml', 'calories')
    list_filter = ('user', 'date')
