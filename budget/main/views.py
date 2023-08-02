#     return context
import copy
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.db.models import Sum, Q
from .models import Expenses, Categories
from .filters import ExpensesFilter
from .utils import create_default_categories

def home(request):
    return render(request, 'main/home.html')


class ExpensesList(LoginRequiredMixin, ListView):
    model = Expenses
    template_name = 'expenses_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)  # Zmieniono na user_id
        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = ExpensesFilter(self.request.GET, queryset=self.get_queryset())
        # context['filter'] = ExpensesFilter(self.request.GET, queryset=self.get_queryset(), user=self.request.user)
        # get query seta sprawdzić - jego filtry - najpierw filtry, potem suma

        if 'start_date' not in self.request.GET:
            today = date.today()
            start_date = today.replace(day=1)
            end_date = today.replace(day=1, month=today.month + 1) - timedelta(days=1)
            context['filter'].form.data['start_date'] = start_date
            context['filter'].form.data['end_date'] = end_date

        context['amount'] = {
            'balance': self.get_queryset().aggregate(Sum('amount'))['amount__sum'] or 0.00,
            'incomes': self.get_queryset().filter(category_id=1).aggregate(Sum('amount'))['amount__sum'] or 0.00,
            'outcomes': self.get_queryset().exclude(category_id=1).aggregate(Sum('amount'))['amount__sum'] or 0.00
        }

        return context


class ExpensesCreate(LoginRequiredMixin, CreateView):
    model = Expenses
    fields = ('amount', 'date', 'category_id', 'description')
    success_url = reverse_lazy('main:expenses')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)  # Zmieniono na user_id
                                                                # user wyświetla tylko swoje wpisy
        return queryset

    def form_valid(self, form):
        form.instance.user_id = self.request.user  # Przypisanie aktualnie zalogowanego użytkownika
        return super().form_valid(form)


class ExpensesUpdate(LoginRequiredMixin, UpdateView):
    model = Expenses
    fields = ('amount', 'date', 'category_id', 'description')
    success_url = reverse_lazy('main:expenses')

    def form_valid(self, form):
        form.instance.user_id = self.request.user  # Przypisanie aktualnie zalogowanego użytkownika
        return super().form_valid(form)


class ExpensesDelete(LoginRequiredMixin, DeleteView):
    model = Expenses
    success_url = reverse_lazy('main:expenses')

    # def form_valid(self, form):
    #     form.instance.user_id = self.request.user  # Przypisanie aktualnie zalogowanego użytkownika
    #     return super().form_valid(form)


@login_required
def category_list_view(request):
    user = request.user
    categories_list = Categories.objects.filter(Q(user_id=user) | Q(is_default=True, user_id=None))

    if not categories_list.exists():
        create_default_categories(user)

    return render(request, 'main/category_list.html', context={'categories_list': categories_list})

@login_required
def category_add_view(request):
    if request.method == "GET":
        return render(request, 'main/category_add_form.html')

    if request.method == "POST":
        category_name = request.POST.get('category_name')
        user = request.user

        # Sprawdź, czy kategoria już istnieje dla użytkownika
        if not Categories.objects.filter(user_id=user, name=category_name).exists():
            category = Categories(name=category_name, user_id=user)
            category.save()


        return redirect("main:category_list_view")


@login_required
def category_detail_view(request, pk):
    user = request.user
    category = get_object_or_404(Categories, id=pk, user_id=user)
    return render(request, 'main/category_detail.html', context={'category': category})


@login_required
def category_update_view(request, pk):
    user = request.user
    category = get_object_or_404(Categories, id=pk, user_id=user)

    if category.name == "Przychody":
        return render(request, 'main/category_update_message.html')

    if request.method == "GET":
        return render(request, 'main/category_update.html', context={'category': category})
    if request.method == "POST":
        category_new_name = request.POST.get('category')
        categories_list = Categories.objects.filter(Q(user_id=user) | Q(user_id=None))
        other_filters = ['Przychody']
        other_filters_boolean = any([category.name in other_filters for category in categories_list])
        if (not categories_list.filter(name=category_new_name).exclude(id=pk).exists()) and other_filters_boolean:
            category.name = category_new_name
            category.save()
        return redirect("main:category_list_view")


# user nie może usunąć/zmienic kategorii nawet tych nowo dodanych, ale poprawnie się wszystko wyświetla
@login_required
def category_delete_view(request, pk):
    user = request.user
    category = get_object_or_404(Categories, id=pk, user_id=user)

    if category.name == "Przychody":
        return render(request, 'main/category_delete_message.html')

    if request.method == "GET":
        return render(request, 'main/category_confirm_delete.html', context={'category': category})

    if request.method == "POST":
        res = request.POST.get('accept')
        if res:
            categories_list = Categories.objects.filter(Q(user_id=user) | Q(user_id=None))
            other_filters = ['Przychody']
            # a wystarczyło tutaj tylko usunąc not <facepalm>
            other_filters_boolean = any([category.name in other_filters for category in categories_list])
            if other_filters_boolean:
                category.delete()
            return redirect("main:category_list_view")

    # Obsługa żądania POST, jeśli przycisk "Anuluj" został kliknięty
    return redirect("main:category_list_view")
