from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core import consts


class Profile(models.Model):
    first_name = models.CharField(verbose_name='name', blank=False, max_length=20)
    second_name = models.CharField(verbose_name='second_name', blank=False, max_length=20)
    date_of_registration = models.DateTimeField(verbose_name='date_of_registration', auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    email = models.EmailField(verbose_name='email', blank=False, max_length=255)
    phone = PhoneNumberField(verbose_name='phone', blank=False)
    role = models.CharField(choices=consts.CHOISES, default='customer', max_length=15)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ['user']

    def __str__(self) -> str:
        return f'{self.first_name} {self.second_name}'


class Restaurant(models.Model):
    name = models.TextField(verbose_name='restaurant', blank=False, max_length=20)
    address = models.TextField(verbose_name='address', blank=False, max_length=50)
    description = models.TextField(verbose_name='restaurant_description', blank=False, max_length=255)

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'
        ordering = ['name']

    def __str__(self) -> str:
        return f'The restaurant {self.name} is located at {self.address}. Discription: {self.description[:100]}'


class Dish(models.Model):
    name = models.CharField(verbose_name='dish_name', blank=False, max_length=20)
    description = models.CharField(verbose_name='dish_description', blank=False, max_length=255)
    price = models.DecimalField(verbose_name='price', max_digits=5, decimal_places=2, blank=False)
    image = models.ImageField(verbose_name='dish_image', upload_to='media/', blank=False)

    class Meta:
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'
        ordering = ['name']

    def __str__(self) -> str:
        return f'Dish {self.name}, price - {self.price}, description - {self.description[:100]}'


class Comment(models.Model):
    text = models.TextField(verbose_name='text_of_comment', blank=False)
    written_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author_of_order')
    dish = models.ForeignKey(
        Dish, related_name='comments', null=True, on_delete=models.CASCADE, verbose_name='comment_of_dish'
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-written_at']

    def __str__(self) -> str:
        return f'{self.author.username} : {self.text[:100]}'


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='customer')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restaurant')
    order_date = models.DateTimeField(verbose_name='date_of_order', auto_now_add=True)
    status = models.CharField(verbose_name='status', max_length=15)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['restaurant']

    def __str__(self) -> str:
        return f'The order {self.id} from {self.restaurant} has status {self.status}'


class Like(models.Model):
    dish = models.ForeignKey(Dish, related_name='likes', on_delete=models.CASCADE, verbose_name='dish')
    profile = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='customer')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dish', 'profile')
        verbose_name = 'like'
        verbose_name_plural = 'likes'
        ordering = ['-liked_at']

    def __str__(self) -> str:
        return f'{self.profile.first_name} {self.profile.second_name} liked {self.dish.text[:100]}'
