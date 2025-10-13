import pytest
from django.utils.timezone import now
from core.models import Profile, Restaurant, Dish, Like, Comment, Order, OrderItem
from decimal import Decimal


@pytest.mark.django_db
def test_profile_customer_creation(django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='123456')
    registration_date = now()
    profile = Profile.objects.create(
        user=user,
        first_name='test',
        second_name='test',
        date_of_registration=registration_date,
        email='test@test.ru',
        phone='+79613569676',
        role='customer'
    )
    assert profile.user == user
    assert profile.first_name == 'test'
    assert profile.second_name == 'test'
    assert profile.date_of_registration.replace(microsecond=0) == registration_date.replace(microsecond=0)
    assert profile.email == 'test@test.ru'
    assert profile.phone.as_e164 == '+79613569676'
    assert profile.role == 'customer'


@pytest.mark.django_db
def test_profile_restaurant_creation(django_user_model):
    user = django_user_model.objects.create_user(username='testuser2', password='123456')
    registration_date = now()
    profile = Profile.objects.create(
        user=user,
        first_name='rest',
        second_name='rest',
        date_of_registration=registration_date,
        email='test@test.ru',
        phone='+79613569676',
        role='restaurant',
    )
    assert profile.user == user
    assert profile.first_name == 'rest'
    assert profile.second_name == 'rest'
    assert profile.date_of_registration.replace(microsecond=0) == registration_date.replace(microsecond=0)
    assert profile.email == 'test@test.ru'
    assert profile.phone.as_e164 == '+79613569676'
    assert profile.role == 'restaurant'

@pytest.mark.django_db
def test_dish_creation(django_user_model):
    user = django_user_model.objects.create_user(username='test', password='123456')
    profile = Profile.objects.create(
        first_name='test',
        second_name='test',
        user=user,
        email='test@test.com',
        phone='+1234567890',
        role='restaurant'
    )
    restaurant = Restaurant.objects.create(
        name='test',
        address='test test',
        description='Nice',
        profile=profile
    )
    dish = Dish.objects.create(
        name='test',
        description='test test',
        price=Decimal('10.50'),
        image='test.png',
        restaurant=restaurant
    )
    assert dish.name == 'test'
    assert dish.price == Decimal('10.50')


@pytest.mark.django_db
def test_restaurant_creation(user_with_profile_restaurant):
    user, profile = user_with_profile_restaurant
    restaurant = Restaurant.objects.create(
        name='test',
        address='test address',
        description='test description',
        profile=profile
    )
    assert restaurant.profile == profile

@pytest.mark.django_db
def test_profile_str(user_with_profile_customer):
    user, profile = user_with_profile_customer
    assert str(profile) == 'customer customer'


@pytest.mark.django_db
def test_comment_creation(user_with_profile_customer):
    user, profile = user_with_profile_customer
    restaurant = Restaurant.objects.create(
        name='Test Restaurant',
        address='123 Test Ave',
        description='A test restaurant',
        profile=profile
    )
    dish = Dish.objects.create(
        name='Test Dish',
        description='Delicious test dish',
        price=Decimal('15.99'),
        image='test.png',
        restaurant=restaurant
    )
    comment = Comment.objects.create(
        text='Great dish!',
        author=user,
        dish=dish
    )
    assert comment.text == 'Great dish!'


@pytest.mark.django_db
def test_order_and_orderitem_creation(user_with_profile_customer):
    user, profile = user_with_profile_customer
    restaurant = Restaurant.objects.create(
        name='Order Restaurant',
        address='234 Test Blvd',
        description='Another test restaurant',
        profile=profile
    )
    order = Order.objects.create(
        profile=profile,
        restaurant=restaurant,
        status='pending'
    )
    dish = Dish.objects.create(
        name='Order Dish',
        description='Order dish description',
        price=Decimal('9.99'),
        image='test_order.png',
        restaurant=restaurant
    )
    order_item = OrderItem.objects.create(
        order=order,
        dish=dish,
        quantity=3
    )
    assert order.status == 'pending'
    assert order_item.quantity == 3
    assert str(order_item).startswith('3 x Order Dish')


@pytest.mark.django_db
def test_like_creation(user_with_profile_customer):
    user, profile = user_with_profile_customer
    restaurant = Restaurant.objects.create(
        name='Like Restaurant',
        address='345 Test St',
        description='Restaurant for likes',
        profile=profile
    )
    dish = Dish.objects.create(
        name='Liked Dish',
        description='Delicious dish',
        price=Decimal('12.99'),
        image='liked_dish.png',
        restaurant=restaurant
    )
    like = Like.objects.create(
        dish=dish,
        profile=user
    )
    assert like.dish == dish
    assert like.profile == user
