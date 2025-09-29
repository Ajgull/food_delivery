from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, View

from core.forms import UserLoginForm, UserRegistrationForm
from core.models import Dish


class DishesListView(ListView):
    model = Dish
    template_name = 'core/dishes.html'
    context_object_name = 'dishes'


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user_form = UserRegistrationForm()
        return render(request, 'core/register.html', {'user_form': user_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'core/dishes.html', {'user_form': user_form})
        return render(request, 'core/register.html', {'user_form': user_form})


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user_form = UserLoginForm()
        return render(request, 'core/login.html', {'user_form': user_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            username = user_form.cleaned_data['username']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                user_form.add_error(username, 'Profile not exists!!!\n Please, register.')
        return render(request, 'core/login.html', {'user_form': user_form})
