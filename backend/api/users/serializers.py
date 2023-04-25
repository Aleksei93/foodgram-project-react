import djoser.serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import (Subscription)

User = get_user_model()

class CustomUserCreateSerializer(djoser.serializers.UserCreateSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())

    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')
        model = User


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if 'request' not in self.context:
            return False

        if not self.context['request'].user.is_authenticated:
            return False

        return Subscription.objects.filter(
            author=obj, user=self.context['request'].user).exists()

    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        model = User
