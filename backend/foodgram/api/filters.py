from django.db.models import Q
from django_filters import rest_framework as django_filters
from rest_framework import filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        name='tags__slug',
        to_field_name='name',
        lookup_type='in',
        queryset=Recipe.objects.all()
        )
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart')
    is_favorited = django_filters.BooleanFilter(
        field_name='is_favorited', method='filter_is_favorited')

    def filter_tags(self, queryset, name, value):
        values = self.request.GET.getlist(key='tags', default=[])

        if not value:
            return queryset

        queries = [Q(tags__slug=value) for value in values]

        query = queries.pop()
        for item in queries:
            query |= item

        return queryset.filter(query).distinct()

    def __is_something(self, queryset, name, value, related_field):
        if self.request.user.is_anonymous:
            return Recipe.objects.none() if value else queryset

        objects = getattr(self.request.user, related_field).all()
        return queryset.filter(pk__in=[item.recipe.pk for item in objects])

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.__is_something(queryset, name, value, 'shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        return self.__is_something(queryset, name, value, 'favorites')

    class Meta:
        model = Recipe
        fields = ('author',)


class IngredientsSearchFilter(filters.SearchFilter):
    search_param = 'name'
