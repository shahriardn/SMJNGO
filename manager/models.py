from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models import Sum
from django_jalali.db import models as jmodels
from persiantools import characters, digits
import os


CURRENCY = 'تومان'

# ------------- Categories -------------- #
# ========================================#

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان صندوق")
    balance = models.IntegerField(default=0, verbose_name="سرمایه")

    class Meta:
        verbose_name_plural = 'صندوق و خزانه'

    def __str__(self):        
        return self.title

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'

    tag_balance.short_description = 'مقدار'


    def Update_Category(self):
        queryset_Inc = self.Income_Cat.all()
        queryset_Exp = self.Expense_Cat.all()
        income_Value = queryset_Inc.aggregate(Sum('amount'))['amount__sum'] if queryset_Inc else 0
        expese_Value = queryset_Exp.aggregate(Sum('amount'))['amount__sum'] if queryset_Exp else 0
        self.balance = income_Value - expese_Value
        self.save()


class PaymentMethod(models.Model):
    title = models.CharField(unique=True, max_length=150, verbose_name="عنوان")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'روشهای پرداخت'



# --------- Person Models ----------- #
#-------------------------------------

#---------- Abstract Class Person -------
class PersonalInfo(models.Model):
    f_name = models.CharField(max_length=20, null=True, verbose_name="نام")
    l_name = models.CharField(max_length=40, null=True, verbose_name="نام خانوادگی")
    address = models.TextField(default="اصفهان", verbose_name="آدرس محل سکونت")
    job = models.CharField(max_length=20, null=True,default="بی کار", verbose_name="شغل")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    verbose_name="شماره تلفن")  # validators should be a list
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        null=True,
        default="F",
        verbose_name="جنسیت"
    )
    description = models.TextField(default="مددجو",verbose_name="توضیحات بیشتر")
    is_arab = models.BooleanField(default=False,verbose_name="سید؟")

    class Meta:
        abstract = True

#------------ Volunteer -----------
class Volunteer(PersonalInfo):
    Join_CHOICES = (
        ('T', 'Telegram',),
        ('W', 'WebSite',),
        ('I', 'Instagram'),
        ('F','FriendRelation'),
    )
    join_by = models.CharField(
        max_length=1,
        choices=Join_CHOICES,
        null=True,
        default="F",
        verbose_name="نحوه آشنایی"
    )

    def __str__(self):
        return "%s, %s"%(self.f_name,self.l_name)

    class Meta:
        verbose_name_plural = 'نیکوکاران'

#------------ Madadjoo -------------
class Madadjoo(PersonalInfo):
    sonat_religion = models.BooleanField(verbose_name="سنی")
    Nation_CHOICES = (
        ('IR', 'ایرانی'),
        ('Af', 'افقان',),
        ('Pa', 'پاکستان',),
    )
    nationality = models.CharField(
        max_length=2,
        choices=Nation_CHOICES,
        verbose_name="ملیت",
        default="IR"
    )

    def __str__(self):
        return "%s, %s"%(self.f_name,self.l_name)

    class Meta:
        verbose_name_plural = 'مددجویان'

    # ---------- Budget ------------- #
    # =================================
    # ----------Transaction --------#

class Transaction(models.Model):
    title = models.CharField(max_length=40,null=True, verbose_name='عنوان')
    objects = jmodels.jManager()
    date = jmodels.jDateField(verbose_name='تاریخ')
    amount = models.IntegerField(verbose_name='مقدار')
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL, verbose_name='پرداخت با')

    class Meta:
        abstract = True

    def tag_date(self):
        return  "%s"%(digits.en_to_fa(self.date.__str__()))


    # ----------- Expense ---------------- #

class Expense(Transaction):
    madadjoo = models.ForeignKey(Madadjoo, on_delete=models.CASCADE,default=1, verbose_name='شخص استفاده کننده')
    discription = models.TextField(verbose_name='توضیحات', blank=True)
    paid_for = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='Expense_Cat', verbose_name='پرداخت برای')

    class Meta:
        verbose_name_plural = 'هزینه و خرج'

    def delete_model(modeladmin, request, queryset, self):
        self.paid_for.Update_Category()
        for obj in queryset:
            filename = obj.profile_name + ".xml"
            os.remove(os.path.join(obj.type, filename))
            obj.delete()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        self.modified = timezone.now()
        super(Expense, self).save(*args, **kwargs)
        self.paid_for.Update_Category()

    def __str__(self):
        return self.title

    def tag_balance(self):
        return f'{digits.en_to_fa(self.amount.__str__())} {CURRENCY}'

    tag_balance.short_description = 'مقدار'



# ----------- Income ---------------#

class Income(Transaction):
    volunteer = models.ForeignKey(Volunteer,
                                  on_delete=models.CASCADE,
                                  verbose_name='خیر')
    paid_for = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='Income_Cat',
                                 verbose_name='پرداخت برای')

    class Meta:
        verbose_name_plural = 'واریز و دریافت'

    def __str__(self):        
        return self.title

    def delete_model(modeladmin, request, queryset, self):
        for obj in queryset:
            filename = obj.profile_name + ".xml"
            os.remove(os.path.join(obj.type, filename))
            self.paid_for.Update_Category()

    def save(self, *args, **kwargs):
        super(Income, self).save(*args, **kwargs)
        self.paid_for.Update_Category()

    def tag_balance(self):
        return f'{digits.en_to_fa(self.amount.__str__())} {CURRENCY}'

    tag_balance.short_description = 'مقدار'