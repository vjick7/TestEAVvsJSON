from django.contrib import admin

from eav_products.models import ProductEAV, AttributeValue, ProductAttribute, ProductAttributeOption, Category


# Register your models here.

class AttributeValueAdmin(admin.TabularInline):
    model = AttributeValue


@admin.register(ProductAttributeOption)
class ProductAttributeOptionAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'category')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(ProductEAV)
class ProductEAVAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    inlines = [
        AttributeValueAdmin
    ]

    #TODO::After testing override a product Form (Hide attributes on createion), Show up if form changes. Or use JS to open OptionGroupAttributes when category is changing.
    def save_model(self, request, obj, form, change):
        opts = ProductAttributeOption.objects.filter(category_id=obj.category)
        super().save_model(request, obj, form, change)
        for option in opts:
            if not AttributeValue.objects.filter(product_id=obj.id).filter(attribute_id=option.attribute.id).exists():
                attr = AttributeValue()
                attr.product = obj
                attr.attribute = option.attribute
                attr.value = '100'  # TODO:: Add default value to the
                attr.save()
