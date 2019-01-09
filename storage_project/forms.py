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


class CompanyOrderForm(forms.ModelForm):
    article_name = forms.ModelChoiceField(queryset=Article.objects.all(),
                                          widget=forms.Select(attrs={
                                              'class': "product_class form-control",
                                              'id': 'product_id',
                                              'autocomplete': 'off',
                                              'style': 'width:50%'
                                          }))

    class Meta:
        model = SellQuery
        fields = ['company']
        labels = {
            'company': 'Избери фирма'
        }

    def __init__(self, *args, **kwargs):
        super(CompanyOrderForm, self).__init__(*args, **kwargs)



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields