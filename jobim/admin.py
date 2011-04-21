from django.contrib import admin

from lojinha.models import Category, Product, Photo, Bid, Contact


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class PhotoInline(admin.TabularInline):
    model = Photo


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'sold')
    list_filter = ('category', 'sold')

    inlines = [PhotoInline]
    prepopulated_fields = {'slug': ('name',)}


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('product', 'pk')


class BidAdmin(admin.ModelAdmin):
    list_display = ('product', 'value', 'mail', 'accepted')
    list_filter = ('product', 'accepted')

    actions = ['accept_bid']

    def accept_bid(self, request, queryset):
        queryset.update(accepted=True)
    accept_bid.short_description = u'Aceitar lances selecionados'


class ContactAdmin(admin.ModelAdmin):
    list_display = ('read', 'name', 'email', 'phone', 'subject')
    list_filter = ('read',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Contact, ContactAdmin)
