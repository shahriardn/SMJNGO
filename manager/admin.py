from django.contrib import admin
from .models import *
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
    


class IncomAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    actions = ['delete_modelll']
    list_filter = (
            ('date', JDateFieldListFilter),
        )
    list_display = ['title', 'tag_balance', 'tag_date']


class ExpenseAdmin(admin.ModelAdmin):
    actions = ['delete_model']
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