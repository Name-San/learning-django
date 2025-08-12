from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from tags.models import TaggedItem
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "username", "email", "password1", "password2",),
            },
        ),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1

class Custom_ProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]

admin.site.unregister(Product)
admin.site.register(Product, Custom_ProductAdmin)