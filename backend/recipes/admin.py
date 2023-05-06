from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from recipes.models import (Favorite, Ingredient, IngredientRecipeRelation,
                            Recipe, ShoppingCart, Subscription, Tag)


class FavoriteAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


class ShoppingCartAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


class IngredientRecipeRelationAdminInline(admin.TabularInline):
    model = IngredientRecipeRelation
    exrta = 3


class RecipeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count')
    search_fields = ('name', 'author__username', 'author__last_name',
                     'tags__name', 'tags__slug', 'author__first_name')
    inlines = (IngredientRecipeRelationAdminInline,)

    fieldsets = (
        ('Основнвые данные', {
            'fields': (
                'name', 'author', 'image', 'tags'
            )
        }),
        ('Приготовление', {
            'fields': (
                'text', 'cooking_time',
            )
        }),
    )

    def favorite_count(self, obj):
        return obj.favorites.count()

    def shoppingcart_count(self, obj):
        return obj.shopping_cart.count()

    favorite_count.short_description = 'В избранном'
    shoppingcart_count.short_description = 'В списке покупок'


class IngredeintAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'measurement_unit')


admin.site.register(Ingredient, IngredeintAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
