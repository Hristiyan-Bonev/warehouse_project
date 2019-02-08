from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Category, Warehouse,Order, Company, Delivery, Article, Provider


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('id',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    exclude = ('id',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ('company_id',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    exclude = ('id',)

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    exclude = ('id',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('article_id',)
    filter_horizontal = ('category', 'warehouse')

    def save_model(self, request, obj, form, change):
        import ipdb;ipdb.set_trace()
        # obj.pk = Article.objects.count() + 1
        super(ArticleAdmin, self).save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)