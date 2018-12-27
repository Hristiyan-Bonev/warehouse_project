from django.views.generic import ListView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Article, Company
from .forms import AddArticleForm, AddCompanyForm


class IndexView(TemplateView):
    template_name = 'index.html'


class QuantityListView(ListView):
    template_name = 'quantity_list.html'
    model = Article

    def get_context_data(self, **kwargs):
        articles = Article.objects.all()
        context = super().get_context_data(**kwargs)
        context['articles'] = articles
        return context


class CompanyListView(ListView):
    template_name = 'companies_list.html'
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        context['companies'] = companies
        return context


class AddArticleView(CreateView):
    model = Article
    success_url = reverse_lazy('add_item')
    form_class = AddArticleForm
    template_name = 'add_item.html'


class AddCompanyView(CreateView):
    model = Company
    success_url = reverse_lazy('add_company')
    form_class = AddCompanyForm
    template_name = 'add_company.html'

