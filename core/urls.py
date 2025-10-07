from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from core.views import (
    AddToCartView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    DishCreateView,
    DishDeleteView,
    DishDetailView,
    DishListView,
    DishUpdateView,
    LikeDishView,
    LoginView,
    RegisterView,
    RemoveFromCartView,
    UnlikeDishView,
)

urlpatterns = [
    path('', DishListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),
    path('dish/create/', DishCreateView.as_view(), name='dish_create'),
    path('dish/update/<int:pk>/', DishUpdateView.as_view(), name='dish_update'),
    path('dish/delete/<int:pk>/', DishDeleteView.as_view(), name='dish_delete'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('comment/create/<int:pk>', CommentCreateView.as_view(), name='comment_create'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('dish/<int:pk>/like/', LikeDishView.as_view(), name='like_dish'),
    path('dish/<int:pk>/unlike/', UnlikeDishView.as_view(), name='unlike_dish'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
