from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path, reverse

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
    def get_urls(self):
        return [
            path(
                '<int:pk>/pdf/',
                self.admin_site.admin_view(formPDF.as_view()),
                name='form_payment_pdf',
            ),
        ] + super().get_urls()

    # Transactions processing actions
    def make_processed(modeladmin, request, queryset):
        queryset.update(processed=True)
    make_processed.short_description = "Mark selected transactions as processed"

    def make_not_processed(modeladmin, request, queryset):
        queryset.update(processed=False)
    make_not_processed.short_description = "Mark selected transactions as not processed"

    def download_form_action(self, obj):
        return format_html(
            '<a class="button" href="{}">PDF</a>',
            reverse('admin:form_payment_pdf', args=[obj.pk]),
        )


    list_display = ['__str__', 'processed']
    list_filter = ['processed']
    actions = [make_processed, make_not_processed]
