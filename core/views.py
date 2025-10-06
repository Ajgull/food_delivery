from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from core.cart import Cart
from core.forms import UserLoginForm, UserRegistrationForm
from core.models import Comment, Dish, Like, Order, Profile


def get_user_groups(user: User) -> dict:
    return {
        'is_restaurant': user.groups.filter(name='Restaurant').exists(),
        'is_customer': user.groups.filter(name='Customer').exists(),
        'is_courier': user.groups.filter(name='Courier').exists(),
    }


class LogoutView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('home')


class DishListView(ListView):
    model = Dish
    template_name = 'core/dishes.html'
    context_object_name = 'dishes'

    # def get_context_data(self, **kwargs: str) -> dict:
    #     context = super().get_context_data(**kwargs)
    #     user_groups = get_user_groups(self.request.user)
    #     context.update(user_groups)
    #     return context

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
            register_form.save()
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


class DishCreateView(CreateView):
    model = Dish
    fields = ['name', 'price', 'description', 'image']
    template_name = 'core/dish_create_rest.html'

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class DishDetailView(DetailView):
    model = Dish
    template_name = 'core/dish.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        dish = self.object
        # context['user_has_liked'] = Like.objects.filter(post=post, author=self.request.user).exists()
        context['comments'] = Comment.objects.filter(dish=dish)
        return context


class DishUpdateView(UpdateView):
    model = Dish
    template_name = 'core/dish_update.html'
    fields = '__all__'

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'core/dish_delete.html'

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


# class CommentUpdateView(UpdateView):
#     model = Comment
#     template_name = 'core/comment_update.html'
#     fields = ['text']
#     context_object_name = 'comment'

#     def get_object(self) -> Comment:
#         return get_object_or_404(Comment, pk=self.kwargs.get('pk'), author=self.request.user)

#     def get_success_url(self) -> str:
#         return reverse_lazy('posts')


# class CommentDeleteView(DeleteView):
#     model = Comment
#     template_name = 'core/comment_delete.html'

#     def get_object(self) -> Comment:
#         return get_object_or_404(Comment, pk=self.kwargs.get('pk'), author=self.request.user)

#     def get_success_url(self) -> str:
#         return reverse_lazy('posts')


# class CommentListView(ListView):
#     model = Comment
#     template_name = 'core/comments.html'
#     context_object_name = 'comments'

#     def get_queryset(self) -> QuerySet[Comment]:
#         post_id = self.kwargs.get('post_id')
#         post = get_object_or_404(Post, id=post_id)
#         return Comment.objects.filter(post=post)

#     def get_context_data(self, **kwargs: dict) -> dict:
#         context = super().get_context_data(**kwargs)
#         post_id = self.kwargs.get('post_id')
#         context['post'] = get_object_or_404(Post, id=post_id)
#         return context


# class LikePostView(View):
#     def post(self, request: HttpRequest, post_id: int) -> HttpResponse:
#         post = get_object_or_404(Post, id=post_id)
#         Like.objects.get_or_create(post=post, author=request.user)
#         return redirect('post_detail', pk=post.id)
