from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from main.utils import create_default_categories


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})


from django.urls import reverse
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            create_default_categories(request.user)  # Dodaj wywołanie funkcji create_default_categories() po rejestracji
            # return redirect('login')
            return redirect(reverse('accounts:login'))
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
