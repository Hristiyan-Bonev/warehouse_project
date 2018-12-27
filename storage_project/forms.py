from django import forms
from .models import Article, Company


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


class QueryForm(forms.ModelForm):
    pass