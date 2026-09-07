from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('carriere/offres-emploi/', views.careers_jobs, name='careers_jobs'),
    path('carriere/candidature-spontanee/', views.careers_spontaneous, name='careers_spontaneous'),
    path('bons-plans/', views.bon_plan, name='bon_plan'),
    path('contact/', views.contact, name='contact'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
]
