from django.views.generic import ListView, TemplateView, CreateView, FormView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from .models import Article, Company, Order, CustomUser
from .forms import AddArticleForm, AddCompanyForm, CompanyOrderForm, CustomUserCreationForm
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
    model = Order
    success_url = reverse_lazy('new_order')
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
        form = CompanyOrderForm(data=request.POST)
        products = [x for x in self.request.POST if 'product' in x]
        import ipdb;
        ipdb.set_trace()
        query_data = {}
        if form.is_valid():
            for product in products:
                product_pk, requested_quantity= self.request.POST.get(product, None).split('_')
                print(requested_quantity)
                search_product = Article.objects.get(pk=product_pk)
                search_product.quantity -= int(requested_quantity)
                search_product.save()

                query_data[search_product.pk] = int(requested_quantity)

            form.order_list = json.dumps(query_data)
            form.seller_id = CustomUser.objects.get(id=1).first_name
            form.save()

        else:
            return render(request, self.template_name, {'form': form})
        return HttpResponseRedirect('/add_company/')

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.seller_id = self.request.user


class CreateAcountView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'sign_up.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('create_acount'))


def get_articles(request):

    if request.is_ajax():
        data = request.GET.get('term', '').encode('utf-8').decode('utf-8')  # Workaround for cyrillic
        articles_lower = Article.objects.filter(article_name__icontains=data.lower())
        articles_upper = Article.objects.filter(article_name__icontains=data.title())
        articles = articles_lower | articles_upper

        results = []
        for article in articles:
            article_json = {}
            article_json.update({
                'id': article.pk,
                'label': article.article_name,
                'value': article.quantity,
                'price': float(article.price)
            }) 
            results.append(article_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
