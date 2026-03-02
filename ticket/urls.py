from django.urls import path
from . import views

urlpatterns = [
    # URL pour ton Dashboard (gestion interne)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # URL pour le portail client (soumission de ticket)
    path('', views.soumettre_ticket, name='soumettre_ticket'),

    path('fiche/<int:pk>/', views.fiche_detail, name='fiche_detail'),
    
    
]