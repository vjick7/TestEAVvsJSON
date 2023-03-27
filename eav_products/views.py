from django.db.models import Subquery, Q
from django.shortcuts import render
from django.db import connection

from eav_products.models import ProductEAV, ProductAttribute, AttributeValue, Category, ProductAttributeOption


# Create your views here.
def product_list(request, category_url):
    ### USING TO FILL TABLE ###
    # ProductEAV.seed_data()
    ### USING TO CLEAR TABLE ###
    # ProductEAV.clear_table()
    category = Category.objects.get(slug=category_url)
    products = ProductEAV.objects.filter(category=category)
    attrOpts = ProductAttributeOption.objects.filter(category=category)
    filter_data={}
    #This way allow to get list of attributes and existed values.
    # TODO::On product - generate a filter form (based on type of attribue, count of existing values and etc.
    # TODO::Optimize sql queries
    for opt in attrOpts:
        filter_data[(opt.attribute.id,opt.attribute.name)]=[attr.value for attr in AttributeValue.objects.filter(Q(product__category=category)&Q(attribute=opt.attribute))]
    print(connection.queries)
    return render(request, 'eav_products/templates/product_list.html', {'products': products, 'filter_data':filter_data})


def category_list(request):
    ### USING TO FILL TABLE ###
    # ProductEAV.seed_data()
    ### USING TO CLEAR TABLE ###
    # ProductEAV.clear_table()
    category = Category.objects.all()
    return render(request, 'eav_products/templates/index.html', {'category': category})
