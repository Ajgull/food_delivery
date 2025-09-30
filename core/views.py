from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, View

from core.forms import UserLoginForm, UserRegistrationForm
from core.models import Dish


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
        context['is_restaurant'] = self.request.user.groups.filter(name='Restaurant').exists()
        context['is_customer'] = self.request.user.groups.filter(name='Customer').exists()
        context['is_courier'] = self.request.user.groups.filter(name='Courier').exists()
        print(context['is_restaurant'])
        print(context['is_customer'])
        print(context['is_courier'])
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
    fields = ['name', 'price', 'dexcription', 'image']
    template_name = 'core/dish_create_rest.html'
