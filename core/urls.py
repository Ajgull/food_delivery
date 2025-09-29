from django.contrib import admin
from django.urls import path

from core.views import DishesListView, RegisterView

urlpatterns = [
    path('', DishesListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
]
