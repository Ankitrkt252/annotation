from django.contrib import admin

# Register your models here.
from .models import (
    Detector,
    Frame,
)

class DetectorInline(admin.TabularInline):
    model = Detector

@admin.register(Detector)
class DetectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'w', 'h', 'created', 'updated')

@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    pass