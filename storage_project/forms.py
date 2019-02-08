from django import forms
from .models import Article, Company, Order, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm


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
    company = forms.ModelChoiceField(queryset=Company.objects.all(),
                                          widget=forms.Select(attrs={
                                              'class': "company_class typeahead crispy form-control border-primary",
                                              'id': 'company',
                                              'autocomplete': 'off',
                                              'style': 'width:50%'
                                          }),
                                     label="Избери фирма")

    # seller_id = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
    #                                    widget=forms.Select(attrs={
    #                                        'class': "company_class typeahead form-control border-primary",
    #                                        'id': 'company',
    #                                        'autocomplete': 'off',
    #                                        'style': 'width:50%'
    #                                    }),
    #                                    label="Продавач")
    class Meta:
        model = Order
        fields = ['company']


    def __init__(self, *args, **kwargs):
        super(CompanyOrderForm, self).__init__(*args, **kwargs)



class CustomUserCreationForm(UserCreationForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',)
        field_order = (
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError('This email is already in use.')

    def save(self):
        object = super().save()
        return object

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError('Passwords don\'t match')
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass