from django.urls import path
from . import views

app_name = 'estimated_budget'

urlpatterns = [
    # path('', views.estimated_budget_list, name='estimated'),
    path('', views.EstimatedList.as_view(), name='estimated'),
    path('create/', views.EstimatedCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.EstimatedUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.EstimatedDelete.as_view(), name='delete'),

]