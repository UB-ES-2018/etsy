from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Shop, Product, ProductImage, Options, OptionField, ProductOptions, Tags, ProductTags,\
    Categories
#


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'profile_image')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'has_shop')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductTagsInline(admin.TabularInline):
    model = ProductTags


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductTagsInline, ]


admin.site.register(User, UserAdmin)
admin.site.register(Shop)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOptions)
admin.site.register(Options)
admin.site.register(OptionField)
admin.site.register(Tags)
admin.site.register(Categories)
admin.site.register(ProductImage)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
