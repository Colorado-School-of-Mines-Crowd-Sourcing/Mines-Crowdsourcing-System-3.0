from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Task, Tag, ParticipantCompletedTask

admin.site.unregister(Group)


# Register your models here.
@admin.register(User)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(ParticipantCompletedTask)
class ParticipantCompletedTaskAdmin(admin.ModelAdmin):
    pass
