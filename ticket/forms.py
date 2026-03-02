from django import forms
from .models import Ticket

class ClientTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['client', 'produit', 'description', 'priorite']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priorite': forms.Select(attrs={'class': 'form-select'}),
        }
        