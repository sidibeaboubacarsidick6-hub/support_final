from django.shortcuts import render, redirect
from .models import Ticket, Documentation
from .forms import ClientTicketForm
from django.utils import timezone
import uuid
from django.contrib.auth.decorators import user_passes_test
from .models import Ticket, Documentation


def fiche_detail(request, pk):
    # On récupère la fiche par son ID (pk) ou on affiche une erreur 404 si elle n'existe pas
    from django.shortcuts import get_object_or_404
    documentation = get_object_or_404(Documentation, pk=pk)
    return render(request, 'ticket/fiche_detail.html', {'documentation': documentation})

def soumettre_ticket(request):
    if request.method == "POST":
        import uuid
        # On crée le numéro ici
        num_ticket = "TKT-" + str(uuid.uuid4())[:8].upper()
        
        # On récupère les données du formulaire
        client_nom = request.POST.get('client')
        produit_nom = request.POST.get('produit')
        type_pb = request.POST.get('type_probleme')
        suggestions = request.POST.get('suggestions_autre')

        # On crée l'objet Ticket
        ticket = Ticket(
            numero_ticket=num_ticket,
            client=client_nom,
            produit=produit_nom,
            type_probleme=type_pb,
            suggestions_autre=suggestions,
        )
        
        # L'enregistrement (qui calcule auto la priorité et description)
        ticket.save() 

        # On affiche la page de succès avec l'objet ticket
        return render(request, 'ticket/succes.html', {'ticket': ticket})
    
    # Si ce n'est pas un POST, on affiche juste le formulaire
    return render(request, 'ticket/soumettre_ticket.html')

# 1. On définit la règle de sécurité EN DEHORS du dashboard
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin, login_url='/') # <-- Cette ligne doit être juste au-dessus du 'def dashboard'
def dashboard(request):
    # On récupère les données de base
    total_tickets = Ticket.objects.count()
    
    # Sécurité pour le calcul du taux
    if total_tickets > 0:
        # Assure-toi que 'resolu_par_n1' et 'statut' existent dans ton modèle Ticket
        resolus_n1 = Ticket.objects.filter(resolu_par_n1=True, statut='RESOLU').count()
        taux_n1 = round((resolus_n1 / total_tickets * 100), 1)
    else:
        taux_n1 = 0

    # On récupère le reste
    nb_fiches = Documentation.objects.count()
    en_attente = Ticket.objects.filter(statut='OUVERT').count()
    fiches_liste = Documentation.objects.all().order_by('-cree_le')

    # LE CONTEXTE
    context = {
        'total': total_tickets,
        'taux_n1': taux_n1,
        'nb_fiches': nb_fiches,
        'tickets_en_attente': en_attente, 
        'fiches': fiches_liste,
    }
    return render(request, 'ticket/dashboard.html', context)