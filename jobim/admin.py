from django.contrib import admin

from jobim.models import (
    Category, Product, Photo, Bid, Contact, Store, UserProfile)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

    prepopulated_fields = {'slug': ('name',)}


class PhotoInline(admin.TabularInline):
    model = Photo


class ProductAdmin(admin.ModelAdmin):
    list_display = ('store', 'name', 'slug', 'category', 'status')
    list_filter = ('category', 'status')

    inlines = [PhotoInline]
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('store', )

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ()
        return super(ProductAdmin, self).add_view(
            request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        self.readonly_fields = ('store', )
        return super(ProductAdmin, self).change_view(
            request, object_id, extra_context)

    def queryset(self, request):
        qs = super(ProductAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__userprofile__user=request.user)

    def save_model(self, request, obj, form, change):
        obj.store = Store.objects.get(userprofile__user=request.user)
        return super(ProductAdmin, self).save_model(request, obj, form, change)


class BidAdmin(admin.ModelAdmin):
    list_display = ('accepted', 'datetime', 'product', 'amount', 'email')
    list_filter = ('product', 'accepted')
    readonly_fields = ('datetime', )

    actions = ['accept_bid']

    def accept_bid(self, request, queryset):
        queryset.update(accepted=True)
    accept_bid.short_description = 'Accept selected bids'

    def queryset(self, request):
        qs = super(BidAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(product__store__userprofile__user=request.user)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'store',
        'read',
        'datetime',
        'email',
        'name',
        'subject',
        'phone_number')
    list_filter = ('read',)
    readonly_fields = ('datetime',)

    def queryset(self, request):
        qs = super(ContactAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__userprofile__user=request.user)


class StoreAdmin(admin.ModelAdmin):
    list_display = ('url', 'email', 'name', 'slogan')

    def queryset(self, request):
        qs = super(StoreAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(userprofile__user=request.user)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
