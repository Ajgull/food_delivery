from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, View

from core.forms import UserRegistrationForm
from core.models import Dish


class DishesListView(ListView):
    model = Dish
    template_name = 'core/dishes.html'
    context_object_name = 'dishes'


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = UserRegistrationForm()
        return render(request, 'core/register.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            return render(request, 'core/register_done.html', {'form': form})
        return render(request, 'core/register.html', {'form': form})
