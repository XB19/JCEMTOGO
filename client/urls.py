from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.home, name='home'),
    path('bons-plans/', views.bon_plan, name='bon_plan'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
]
