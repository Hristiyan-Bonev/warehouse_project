from django.views.generic import ListView, TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core import serializers
from .models import Article, Company, SellQuery
from .forms import AddArticleForm, AddCompanyForm, CompanyOrderForm
import json


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


class NewOrderView(FormView):
    model = SellQuery
    success_url = reverse_lazy('new_order')
    # form_class = ProductOrderForm
    template_name = 'new_order.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()


    def get_context_data(self, **kwargs):
        json_serializer = serializers.get_serializer("json")()
        articles = json_serializer.serialize(Article.objects.all(), ensure_ascii=False)
        company_form = CompanyOrderForm(self.request.GET or None)
        context_data = {}
        context_data['company_form'] = company_form
        context_data['articles'] = articles
        return context_data

    def post(self, request, *args, **kwargs):

        products = [x for x in self.request.POST if 'product' in x]
        query_data = {}

        for product in products:
            product_pk, requested_quantity= self.request.POST.get(product, None).split('_')
            print(requested_quantity)
            search_product = Article.objects.get(pk=product_pk)
            # form = ProductOrderForm(instance=search_product)
            search_product.quantity -= int(requested_quantity)
            # search_product.save()

            query_data[search_product.article_name] = int(requested_quantity)

        print(query_data)


def get_articles(request):

    if request.is_ajax():
        data = request.GET.get('term', '').encode('utf-8').decode('utf-8') # Workaround for cyrillic
        articles_lower = Article.objects.filter(article_name__icontains = data.lower())
        articles_upper = Article.objects.filter(article_name__icontains=data.title())
        articles = articles_lower | articles_upper

        results = []
        for article in articles:
            article_json = {}
            # import ipdb;ipdb.set_trace()
            article_json['id'] = article.pk
            article_json['label'] = article.article_name
            article_json['value'] = article.quantity
            article_json['price'] = float(article.price)
            results.append(article_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)