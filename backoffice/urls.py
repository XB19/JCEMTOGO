from django.urls import path

from . import views

app_name = 'backoffice'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('deliveries/', views.deliveries, name='deliveries'),
    path('planning/', views.planning, name='planning'),
    path('trucks/', views.trucks, name='trucks'),
    path('billing/', views.billing, name='billing'),
    path('reports/', views.reports, name='reports'),
    path('new-order/', views.new_order, name='new_order'),
]
