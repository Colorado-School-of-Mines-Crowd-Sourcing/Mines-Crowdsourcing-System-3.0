from django.contrib import admin

from .models import Task, Tag

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass
