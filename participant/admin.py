from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Task, Tag, ParticipantCompletedTask

admin.site.unregister(Group)


# Register your models here.

# User actions
def make_requester(modeladmin, request, queryset):
    queryset.update(authorized_requester=True)
make_requester.short_description = "Mark selected users as authorized requester"

@admin.register(User)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ['authorized_requester']
    actions = [make_requester]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(ParticipantCompletedTask)
class ParticipantCompletedTaskAdmin(admin.ModelAdmin):
    pass
