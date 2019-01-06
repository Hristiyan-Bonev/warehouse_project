from django import forms
from .models import Article, Company, SellQuery, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import modelformset_factory, inlineformset_factory


class AddArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['article_id']
        labels = {
            'article_name': 'Име на артикул',
            'price': 'Цена',
            'quantity': 'Количество'
        }


class AddCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['company_id']
        labels = {
            'company_name': 'Име на фирма',
            'company_address': 'Адрес',
            'bulstat': 'Булстат/ЕИК',
            'responsible_person': 'МОЛ'
        }

    def __init__(self, *args, **kwargs):
        super(AddCompanyForm, self).__init__(*args, **kwargs)

        self.fields['company_name'].error_messages = 'Вече съществува фирма с такова име'
        self.fields['bulstat'].error_messages = 'Вече съществува фирма с такъв булстат'

        # TODO : MAKE ERROR MESSAGES IN BULGARIAN


class ProductOrderForm(forms.ModelForm):

    article_list = forms.ModelChoiceField(queryset=Article.objects.all())
    companies_list = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = Article
        exclude = ('__all__',)


class CompanyOrderForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['company_name']



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields