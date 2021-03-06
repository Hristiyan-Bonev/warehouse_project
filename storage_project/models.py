from django.db import models
from django.contrib.auth.models import AbstractUser,  UserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(UserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user has adnub status.'))
    is_moderator = models.BooleanField(_('moderator status'), default=False,
                                   help_text=_('Designates whether the user has moderator status'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as fired'
                                                ' .Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(unique=True, max_length=100)
    responsible_person = models.CharField(max_length=100)
    bulstat = models.CharField(unique=True, max_length=15)
    company_address = models.CharField(max_length=255)
    company_city = models.CharField(max_length=80)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Provider(models.Model):
    id = models.IntegerField(primary_key=True)
    provider_name = models.CharField(unique=True, max_length=100)
    provider_city = models.CharField(max_length=20)
    provider_address = models.CharField(max_length=20)
    provider_contact_name = models.CharField(max_length=50, blank=True)
    provider_phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.provider_name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Warehouse(models.Model):
    id = models.IntegerField(primary_key=True)
    warehouse_name = models.CharField(unique=True, max_length=50)
    warehouse_city = models.CharField(max_length=100)
    warehouse_address = models.CharField(max_length=100)

    def __str__(self):
        return self.warehouse_name


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_name = models.CharField(unique=True, max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=3)
    quantity = models.IntegerField()
    category = models.ManyToManyField(Category)
    warehouse = models.ManyToManyField(Warehouse)

    def __str__(self):
        return self.article_name


class Order(models.Model):

    CASH = 'Cash'
    LEASE = 'Lease'

    PAYMENT_CHOICES = (
        (CASH, 'Cash'),
        (LEASE, 'Lease')
    )

    id = models.IntegerField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_list = models.ManyToManyField(Article)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=8)
    payment_method = models.CharField(max_length=5, choices=PAYMENT_CHOICES, default=CASH)
    note = models.TextField(max_length=200)

    class Meta:
        managed = True


class Delivery(models.Model):
    id = models.IntegerField(primary_key=True)
    delivery_list = models.ManyToManyField(Article)
    delivery_date = models.DateTimeField(auto_now_add=True)
    delivery_company = models.ForeignKey(Provider, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=8)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note = models.TextField(max_length=200)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'