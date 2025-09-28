from django.views.generic import ListView

from core.models import Dish


class DishesListView(ListView):
    model = Dish
    template_name = 'core/dishes.html'
    context_object_name = 'dishes'
