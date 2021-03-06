"""storage_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import IndexView, QuantityListView, CompanyListView, AddArticleView, AddCompanyView, NewOrderView, get_articles, CreateAcountView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('quantities', QuantityListView.as_view(), name='quantities'),
    path('companies', CompanyListView.as_view(), name='companies'),
    path('add_article', AddArticleView.as_view(), name='add_item'),
    path('add_company', AddCompanyView.as_view(), name='add_company'),
    path('new_order', NewOrderView.as_view(), name='new_order'),
    path('get_articles/', get_articles, name='get_articles'),
    path('sign_up', CreateAcountView.as_view(), name='create_account'),
    # path('login', auth_views.login, {'template_name': 'sign_in.html'}, name='login')
]
