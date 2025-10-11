from rest_framework import serializers

from core import models


class Profile(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'


class Dish(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = '__all__'


class Comment(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class Restaurant(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = '__all__'


class Order(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'


class OrderItem(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'


class Like(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'
