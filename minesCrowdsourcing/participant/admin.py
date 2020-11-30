from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path, reverse
from django.utils.html import format_html

from zipfile import ZipFile

from .models import User, Task, Tag, Transaction
from .views import formPDF

admin.site.unregister(Group)

# Register your models here.

@admin.register(User)
class TaskAdmin(admin.ModelAdmin):

    # User actions
    def make_requester(modeladmin, request, queryset):
        queryset.update(authorized_requester=True)
    make_requester.short_description = "Mark selected users as authorized requester"

    list_filter = ['authorized_requester']
    actions = [make_requester]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
