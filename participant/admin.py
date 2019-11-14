from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Task, Tag, Transaction

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

# Transactions processing actions
def make_processed(modeladmin, request, queryset):
    queryset.update(processed=True)
make_processed.short_description = "Mark selected transactions as processed"

def make_not_processed(modeladmin, request, queryset):
    queryset.update(processed=False)
make_not_processed.short_description = "Mark selected transactions as not processed"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'processed']
    list_filter = ['processed']
    actions = [make_processed, make_not_processed]
