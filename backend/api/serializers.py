import base64
import mimetypes

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from api.ingridients.serializers import IngredientRecipeRelationSerializer
from api.tags.serializers import TagSerializer
from api.users.serializers import CustomUserSerializer
from recipes.models import (Favorite, Ingredient, IngredientRecipeRelation,
                            Recipe, ShoppingCart, Subscription)

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False

        return Subscription.objects.filter(
            author=obj, user=self.context['request'].user).exists()

    class Meta:
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed')
        model = User


class RecipeSerializerList(serializers.ModelSerializer):
    author = AuthorSerializer(required=False, many=False, read_only=True)
    tags = TagSerializer(required=False, many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def __is_something(self, obj, model):
        if not self.context['request'].user.is_authenticated:
            return False

        return model.objects.filter(
            recipe=obj, user=self.context['request'].user).exists()

    def get_is_in_shopping_cart(self, obj):
        return self.__is_something(obj, ShoppingCart)

    def get_is_favorited(self, obj):
        return self.__is_something(obj, Favorite)

    def get_ingredients(self, obj):
        return IngredientRecipeRelationSerializer(
            IngredientRecipeRelation.objects.filter(recipe=obj).all(),
            many=True).data

    class Meta:
        exclude = ('created', )
        model = Recipe


class RecipeCreateIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')
        model = IngredientRecipeRelation


class ImageBase64Field(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            mime_data, image_string = data.split(';base64,')
            image_data = base64.b64decode(image_string)

            mime_type = mime_data.removeprefix('data:')
            extension = mimetypes.MimeTypes().guess_extension(mime_type)

            data = ContentFile(image_data, name=f'temp.{extension}')

        return super().to_internal_value(data)


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = RecipeCreateIngredientSerializer(many=True)
    image = ImageBase64Field()
    author = CustomUserSerializer(required=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def __is_something(self, obj, model):
        if not self.context['request'].user.is_authenticated:
            return False

        return model.objects.filter(
            recipe=obj, user=self.context['request'].user).exists()

    def get_is_in_shopping_cart(self, obj):
        return self.__is_something(obj, ShoppingCart)

    def get_is_favorited(self, obj):
        return self.__is_something(obj, Favorite)

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        obj = Recipe.objects.create(**validated_data)
        obj.save()

        obj.tags.set(tags)

        for ingredient in ingredients:
            IngredientRecipeRelation.objects.create(
                recipe=obj, ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ).save()

        return obj

    def validate(self, data):
        keys = ('ingredients', 'tags', 'text', 'name', 'cooking_time')

        errors = {}

        for key in keys:
            if key not in data:
                errors.update({key: 'Обязательное поле'})

        if errors:
            raise serializers.ValidationError(errors, code='field_error')

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.tags.set(tags)
        instance.image = validated_data.get('image', instance.image)

        instance.ingredients.clear()
        for ingredient in ingredients:
            IngredientRecipeRelation.objects.create(
                recipe=instance, ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ).save()

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields['tags'] = TagSerializer(many=True)

        representation = super().to_representation(instance)

        representation['ingredients'] = IngredientRecipeRelationSerializer(
            IngredientRecipeRelation.objects.filter(
                recipe=instance).all(), many=True).data

        return representation

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipe


class RecipeShortSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'image', 'name', 'cooking_time')
        model = Recipe
