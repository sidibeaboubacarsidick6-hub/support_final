from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Ticket
from .models import Documentation
from datetime import timedelta

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Correction : On utilise bien 'statut_couleur' qui est défini plus bas
    list_display = ('numero_ticket', 'client', 'priorite', 'statut_couleur', 'temps_restant', 'resolu_par_n1')
    list_filter = ('priorite', 'statut', 'resolu_par_n1', 'cree_le')
    search_fields = ('numero_ticket', 'client')
    readonly_fields = ('cree_le',)

    def statut_couleur(self, obj):
        colors = {
            'OUVERT': '#d9534f',  # Rouge
            'EN_COURS': '#f0ad4e', # Orange
            'RESOLU': '#5cb85c',   # Vert
            'ESCALADE': '#5bc0de', # Bleu
        }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors.get(obj.statut, 'black'),
            obj.statut
        )
    # Texte affiché en haut de la colonne
    statut_couleur.short_description = 'Statut'

    def temps_restant(self, obj):
        # Délais basés sur tes objectifs de stage [cite: 126, 127, 128]
        delais = {
            'CRITIQUE': 2,
            'HAUTE': 4,
            'MOYENNE': 24,
            'FAIBLE': 48
        }
        max_hours = delais.get(obj.priorite, 24)
        deadline = obj.cree_le + timedelta(hours=max_hours)
        
        if obj.statut == 'RESOLU':
            return "Terminé"
            
        restant = deadline - timezone.now()
        total_seconds = restant.total_seconds()
        heures = total_seconds / 3600
        
        if total_seconds < 0:
            return format_html('<span style="color:red; font-weight:bold;">SLA Dépassé !</span>')
        return f"{round(heures, 1)}h restantes"
    
    temps_restant.short_description = 'Délai SLA'

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'cree_le', 'mis_a_jour_le')
    list_filter = ('categorie',)
    search_fields = ('titre', 'contenu')