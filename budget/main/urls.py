from django.contrib import admin
from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('expenses/', views.ExpensesList.as_view(), name='expenses'),
    path('create/', views.ExpensesCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.ExpensesUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.ExpensesDelete.as_view(), name='delete'),
    path('category_add/', views.category_add_view, name='category_add_view'),
    path('category_list/', views.category_list_view, name='category_list_view'),  # list
    path('<int:pk>/', views.category_detail_view, name='category_detail_view'),  # detail
    path('update_category/<int:pk>/', views.category_update_view, name='category_update_view'),
    path('delete_category/<int:pk>/', views.category_delete_view, name='category_delete_view'),
]
