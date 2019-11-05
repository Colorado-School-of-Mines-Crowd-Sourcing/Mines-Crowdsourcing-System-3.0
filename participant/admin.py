from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Task, Tag, ParticipantCompletedTask, Transaction

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


# Transactions processing action 
def make_processed(modeladmin, request, queryset):
    queryset.update(processed=True)
make_processed.short_description = "Mark selected transactions as processed"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'processed']
    list_filter = ['processed']
    actions = [make_processed]
