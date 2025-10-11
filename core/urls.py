from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from core.views import (
    AddToCartView,
    CommentAPI,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    DishAPI,
    DishCreateView,
    DishDeleteView,
    DishDetailView,
    DishListView,
    DishUpdateView,
    LikeAPI,
    LikeDishView,
    LoginView,
    OrderAPI,
    OrderItemAPI,
    OrderListView,
    ProfileAPI,
    RegisterView,
    RemoveFromCartView,
    RestaurantAPI,
    UnlikeDishView,
    create_order,
)

router = DefaultRouter()


router.register('profile_api', ProfileAPI, basename='profile_api')
router.register('restaurant_api', RestaurantAPI, basename='restaurant_api')
router.register('dish_api', DishAPI, basename='dish_api')
router.register('comment_api', CommentAPI, basename='comment_api')
router.register('order_api', OrderAPI, basename='order_api')
router.register('order_item_api', OrderItemAPI, basename='order_item_api')
router.register('like_api', LikeAPI, basename='like_api')

urlpatterns = [
    path('', DishListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
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
    path('order/', create_order, name='order'),
    path('order/detail/', OrderListView.as_view(), name='order_list'),
] + router.urls
