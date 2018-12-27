from django.db import models


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(unique=True, max_length=100)
    responsible_person = models.CharField(max_length=100)
    bulstat = models.CharField(unique=True, max_length=15)
    company_address = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    article_name = models.CharField(unique=True, max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=3)
    quantity = models.IntegerField()


class SellQuery(models.Model):
    id = models.IntegerField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    seller = models.CharField(max_length=50)
    order = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)