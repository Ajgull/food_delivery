from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from core.views import DishCreateView, DishListView, LoginView, RegisterView

urlpatterns = [
    path('', DishListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dish/new', DishCreateView.as_view(), name='dish_create'),
]
