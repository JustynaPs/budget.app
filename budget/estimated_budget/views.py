from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from main.models import Categories
from .models import Estimated


class EstimatedList(LoginRequiredMixin, ListView):
    model = Estimated
    template_name = 'estimated_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id)  # Zmieniono na user_id

        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(EstimatedList, self).get_context_data(*args, **kwargs)
        user = self.request.user


        context['amount'] = {'balance': Estimated.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0.00,
                             'incomes': Estimated.objects.filter(category_id__name='Przychody', user=user).aggregate(Sum('amount'))[
                                            'amount__sum'] or 0.00,
                             'outcomes': Estimated.objects.exclude(category_id__name='Przychody',).filter(user=user).aggregate(Sum('amount'))[
                                             'amount__sum'] or 0.00}

        return context



# działające, w razie czego do tego powróć
# @login_required
# def estimated_budget_list(request):
#     user = request.user
#     estimated_list = Estimated.objects.filter(Q(user_id=user))
#
#
#     return render(
#         request,
#         'estimated_budget/estimated_list.html',
#         context={
#             'estimated_list': estimated_list,
#         }
#     )


class EstimatedUpdate(LoginRequiredMixin, UpdateView):
    model = Estimated
    fields = ('amount', 'date', 'category_id', 'description')
    success_url = reverse_lazy('estimated_budget:estimated')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estimated_list'] = Estimated.objects.filter(user=self.request.user)
        return context


# class EstimatedUpdate(LoginRequiredMixin, UpdateView):
#     model = Estimated
#     fields = ('amount', 'date', 'description', 'category_id')
#     success_url = reverse_lazy('estimated_budget:estimated')
#
#     def form_valid(self, form):
#         form.instance.user_id = self.request.user
#         return super().form_valid(form)

class EstimatedCreate(LoginRequiredMixin, CreateView):
    model = Estimated
    fields = ('amount', 'date', 'category_id', 'description')
    success_url = reverse_lazy('estimated_budget:estimated')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estimated_list'] = Estimated.objects.filter(user=self.request.user)
        return context


class EstimatedDelete(LoginRequiredMixin, DeleteView):
    model = Estimated
    success_url = reverse_lazy('estimated_budget:estimated')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user  # Przypisanie aktualnie zalogowanego użytkownika
    #     return super().form_valid(form)


# @login_required
# def category_add_view(request):
#     if request.method == "GET":
#         return render(request, 'main/category_add_form.html')
#
#     if request.method == "POST":
#         category_name = request.POST.get('category_name')
#         user = request.user
#
#         category = Estimated(name=category_name, user_id=user)
#         category.save()
#
#
#         return redirect("estimated_budget:estimated")