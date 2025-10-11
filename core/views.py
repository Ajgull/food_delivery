from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from django_filters.views import FilterView
from rest_framework import viewsets

from core import serializers
from core.cart import Cart
from core.filters import DishFilter
from core.forms import UserLoginForm, UserRegistrationForm
from core.models import Comment, Dish, Like, Order, OrderItem, Profile, Restaurant
from core.tasks import email_send


class ProfileAPI(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.Profile


class RestaurantAPI(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.Restaurant


class DishAPI(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = serializers.Dish


class CommentAPI(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.Comment


class OrderAPI(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.Order


class OrderItemAPI(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItem


class LikeAPI(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = serializers.Like


@login_required
def create_order(request: HttpRequest) -> HttpResponse:
    profile = Profile.objects.get(user=request.user)

    cart = request.session.get('cart', {})
    if cart:
        first_dish_id = next(iter(cart))
        first_dish = Dish.objects.get(id=first_dish_id)
        restaurant = first_dish.restaurant

        order = Order.objects.create(profile=profile, restaurant=restaurant, status='Pending')

        for dish_id, quantity in cart.items():
            dish = Dish.objects.get(id=dish_id)
            OrderItem.objects.create(order=order, dish=dish, quantity=quantity)

        del request.session['cart']
        print(order)

        customer_email = profile.email

        subject = f'New Order #{order.id} Created'

        order_items = OrderItem.objects.filter(order=order)
        items_list = '\n'.join([f'{item.dish.name} x{item.quantity}' for item in order_items])

        message = (
            f'Hello {profile.first_name}, your order #{order.id} has been received.\n\n'
            f'Order items:\n{items_list}\n\n'
            'Thank you for your purchase!'
        )

        email_send.delay(subject, message, [customer_email])

    return redirect('home')


class LogoutView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('home')


class DishListView(FilterView):
    model = Dish
    template_name = 'core/dishes.html'
    context_object_name = 'dishes'
    filterset_class = DishFilter

    def get_context_data(self, **kwargs: str) -> HttpResponse:
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        dishes = []
        total_price = 0
        for dish_id, quantity in cart.items():
            dish = Dish.objects.filter(id=dish_id).first()
            if dish:
                dishes.append({'dish': dish, 'quantity': quantity, 'subtotal': dish.price * quantity})
                total_price += dish.price * quantity
        context['cart_dishes'] = dishes
        context['cart_total_price'] = total_price
        context['cart_total_items'] = sum(cart.values())
        return context


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        register_form = UserRegistrationForm()
        return render(request, 'core/register.html', {'register_form': register_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            profile = user.profile

            if profile.role == 'restaurant':
                restaurant_name = request.POST.get('restaurant_name')
                address = request.POST.get('address')
                description = request.POST.get('restaurant_description')

                if restaurant_name and address and description:
                    from .models import Restaurant

                    Restaurant.objects.create(
                        profile=profile, name=restaurant_name, address=address, description=description
                    )
            return render(request, 'core/dishes.html', {'register_form': register_form})
        return render(request, 'core/register.html', {'register_form': register_form})


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        login_form = UserLoginForm()
        return render(request, 'core/login.html', {'login_form': login_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                login_form.add_error(None, 'Invalid username or password. At views')
        return render(request, 'core/login.html', {'login_form': login_form})


class DishCreateView(UserPassesTestMixin, CreateView):
    model = Dish
    fields = ['name', 'price', 'description', 'image']
    template_name = 'core/dish_create_rest.html'

    def test_func(self) -> bool:
        return self.request.user.profile.role == 'restaurant'

    def form_valid(self, form: Form) -> Form:
        profile = self.request.user.profile

        restaurant = Restaurant.objects.filter(profile=profile).first()
        if not restaurant:
            return self.form_invalid(form)

        form.instance.restaurant = restaurant
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class DishDetailView(DetailView):
    model = Dish
    template_name = 'core/dish.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        dish = self.object
        context['user_has_liked'] = Like.objects.filter(dish=dish, profile=self.request.user).exists()
        context['comments'] = Comment.objects.filter(dish=dish)
        context['restaurant'] = dish.restaurant
        print(f'Dish: {dish.name}, Restaurant: {dish.restaurant}')

        return context


class DishUpdateView(UserPassesTestMixin, UpdateView):
    model = Dish
    template_name = 'core/dish_update.html'
    fields = '__all__'

    def test_func(self) -> bool:
        return self.request.user.profile.role == 'restaurant'

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class DishDeleteView(UserPassesTestMixin, DeleteView):
    model = Dish
    template_name = 'core/dish_delete.html'

    def test_func(self) -> bool:
        return self.request.user.profile.role == 'restaurant'

    def get_object(self) -> Dish:
        return get_object_or_404(Dish, pk=self.kwargs.get('pk'))

    def get_queryset(self) -> QuerySet[Dish]:
        return Dish.objects.filter(dish=self.request.user)

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class AddToCartView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        cart = Cart(request)
        cart.add(pk)
        return redirect('home')


class RemoveFromCartView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        cart = Cart(request)
        cart.remove(pk)
        return redirect('home')


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'core/comment_create.html'
    fields = ['text']

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        pk = self.kwargs['pk']
        dish = get_object_or_404(Dish, id=pk)
        form.instance.author = self.request.user
        form.instance.dish = dish
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('dish_detail', kwargs={'pk': self.object.dish.pk})


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'core/comment_update.html'
    fields = ['text']
    context_object_name = 'comment'

    def get_object(self) -> Comment:
        return get_object_or_404(Comment, pk=self.kwargs.get('pk'), author=self.request.user)

    def get_success_url(self) -> str:
        return reverse_lazy('dish_detail', kwargs={'pk': self.object.dish.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'core/comment_delete.html'

    def get_object(self) -> Comment:
        return get_object_or_404(Comment, pk=self.kwargs.get('pk'), author=self.request.user)

    def get_context_data(self, **kwargs: str) -> dict:
        context = super().get_context_data(**kwargs)
        context['dish'] = self.object.dish
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('dish_detail', kwargs={'pk': self.object.dish.pk})


class OrderListView(ListView):
    model = Order
    template_name = 'core/orders.html'
    context_object_name = 'orders'

    def get_queryset(self) -> QuerySet[Order]:
        return Order.objects.filter(profile__user=self.request.user).order_by('order_date')


class LikeDishView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        dish = get_object_or_404(Dish, id=pk)
        Like.objects.get_or_create(dish=dish, profile=request.user)
        return redirect('dish_detail', pk=dish.pk)


class UnlikeDishView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        dish = get_object_or_404(Dish, id=pk)
        Like.objects.filter(dish=dish, profile=request.user).delete()
        return redirect('dish_detail', pk=dish.pk)
