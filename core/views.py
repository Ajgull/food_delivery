from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from core.forms import UserLoginForm, UserRegistrationForm
from core.models import Dish


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

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        user_groups = get_user_groups(self.request.user)
        context.update(user_groups)
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
    template_name = 'core/dish_detail.html'
    context_object_name = 'dish'


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
