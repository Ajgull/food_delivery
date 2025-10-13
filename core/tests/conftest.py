import pytest
from django.utils.timezone import now
from core.models import Profile

@pytest.fixture(scope="function", autouse=False)
def user_with_profile_customer(django_user_model):
    user = django_user_model.objects.create_user(username="testuser", password="password123")
    profile = Profile.objects.create(
        user=user,
        first_name="customer",
        second_name="customer",
        date_of_registration=now(),
        email="test@test.ru",
        phone="+79613569676",
        role="customer",
    )
    return user, profile

@pytest.fixture(scope="function", autouse=False)
def user_with_profile_restaurant(django_user_model):
    user = django_user_model.objects.create_user(username='testrest', password='password123')
    registration_date = now()
    profile = Profile.objects.create(
        user=user,
        first_name='restaurant',
        second_name='restaurant',
        date_of_registration=registration_date,
        email='test@test.ru',
        phone='+79613569676',
        role='restaurant'
    )
    return user, profile
