import random

from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug+'/'


class ProductEAV(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def clear_table():
        products = ProductEAV.objects.all()
        for product in products:
            product.delete()

    def seed_data():
        for i in range(1000):
            product = ProductEAV()
            product.name = 'product' + str(i)
            product.description = "There're some words about this product"
            product.price = random.random() * i
            product.save()

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    Attribute_Types = [
        ('0', 'Int'),
        ('1', 'Float'),
        ('2', 'Str')
    ]
    name = models.CharField(max_length=20, verbose_name='Attribute name')
    type = models.CharField(max_length=1, choices=Attribute_Types)

    def __str__(self):
        return self.name



class ProductAttributeOption(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class AttributeValue(models.Model):
    product = models.ForeignKey(ProductEAV, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=10)

    def seed_data():
        products = ProductEAV.objects.all()
        attributes = ProductAttribute.objects.all()
        for product in products:
            if (not AttributeValue.objects.filter(product=product).exists()):
                for attr in attributes:
                    attr_value = AttributeValue()
                    attr_value.value = random.randint(1, 100)
                    attr_value.product = product
                    attr_value.attribute = attr
                    attr_value.save()
