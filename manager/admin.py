from django.contrib import admin
from .models import *
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
    


class IncomAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_filter = (
            ('date', JDateFieldListFilter),
        )
    list_display = ['title', 'tag_balance', 'tag_date']

    def delete_queryset(self, request, queryset):
        categories = set(obj.paid_for for obj in queryset if obj.paid_for)
        super().delete_queryset(request, queryset)
        for cat in categories:
            cat.Update_Category()

    def delete_model(self, request, obj):
        category = obj.paid_for
        super().delete_model(request, obj)
        if category:
            category.Update_Category()


class ExpenseAdmin(admin.ModelAdmin):
    list_filter = (
            ('date', JDateFieldListFilter),
        )
    list_display = ['title', 'tag_balance', 'tag_date']
    fieldsets = (
        ("اطلاعات اصلی", {
            'fields': ('title', 'date', 'amount','paid_for')
        }),
        ('توضیحات بیشتر', {
            'classes': ('collapse',),
            'fields': ('discription','madadjoo'),
        }),
    )

    def delete_queryset(self, request, queryset):
        categories = set(obj.paid_for for obj in queryset if obj.paid_for)
        super().delete_queryset(request, queryset)
        for cat in categories:
            cat.Update_Category()

    def delete_model(self, request, obj):
        category = obj.paid_for
        super().delete_model(request, obj)
        if category:
            category.Update_Category()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'tag_balance']



#class ExpenseAdmin(admin.ModelAdmin):
 #   list_display = ['title','tag_date','tag_balance']

admin.site.register(Madadjoo)
admin.site.register(Volunteer)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Income, IncomAdmin)
admin.site.register(PaymentMethod)
