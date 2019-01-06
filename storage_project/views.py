from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Article, Company, SellQuery
from .forms import AddArticleForm, AddCompanyForm, ProductOrderForm, CompanyOrderForm


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


class NewOrderView(ListView):
    model = SellQuery
    success_url = reverse_lazy('new_order')
    # form_class = ProductOrderForm
    template_name = 'new_order.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()


    def get_context_data(self, **kwargs):
        company_form = CompanyOrderForm(self.request.GET or None)
        product_form = ProductOrderForm(self.request.GET or None)
        context_data = super(NewOrderView, self).get_context_data(**kwargs)
        context_data['companies'] = Company.objects.all()
        context_data['company_form'] = company_form
        context_data['product_form'] = product_form
        return context_data


