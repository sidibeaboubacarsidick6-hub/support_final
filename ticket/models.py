from django.db import models
from django.utils import timezone
from datetime import timedelta

class Ticket(models.Model):
    PRODUITS = [
        ('moya_collecte', 'moya collecte'),
        ('ivoire_pass', 'ivoire pass'),
    ]
    
    # --- NOUVEAUX CHAMPS ---
    TYPES_PROBLEMES = [
        ('PANNE_GENERALE', 'Le site/application ne s\'ouvre plus'),
        ('PAIEMENT_ECHOUE', 'Problème de paiement FinTech'),
        ('CONNEXION', 'Impossible de se connecter (Login)'),
        ('LENTEUR', 'L\'application est lente'),
        ('MIS_A_JOUR', 'Bug après une mise à jour'),
        ('AUTRE', 'Autre (Précisez ci-dessous)'),
    ]
    type_probleme = models.CharField(max_length=30, choices=TYPES_PROBLEMES, default='AUTRE')
    suggestions_autre = models.TextField(blank=True, null=True, help_text="Si 'Autre', décrivez ici.")
    # -----------------------

    produit = models.CharField(max_length=20, choices=PRODUITS, default='moya_collecte')
    PRIORITY_CHOICES = [
        ('CRITIQUE', 'Critique (2h)'),
        ('HAUTE', 'Haute (4h)'),
        ('MOYENNE', 'Moyenne (24h)'),
        ('FAIBLE', 'Faible (48h)'),
    ]
    
    STATUS_CHOICES = [
        ('OUVERT', 'Ouvert'),
        ('EN_COURS', 'En cours'),
        ('ESCALADE', 'Escaladé'),
        ('RESOLU', 'Résolu'),
    ]

    numero_ticket = models.CharField(max_length=20, unique=True)
    client = models.CharField(max_length=100)
    description = models.TextField()
    priorite = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MOYENNE')
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OUVERT')
    cree_le = models.DateTimeField(auto_now_add=True)
    resolu_par_n1 = models.BooleanField(default=True)
    date_resolution = models.DateTimeField(null=True, blank=True)

    # --- LOGIQUE AUTOMATIQUE ---

    def save(self, *args, **kwargs):
        # 1. Automatisation de la priorité
        mapping_priorite = {
            'PANNE_GENERALE': 'CRITIQUE',
            'PAIEMENT_ECHOUE': 'HAUTE',
            'CONNEXION': 'HAUTE',
            'MIS_A_JOUR': 'MOYENNE',
            'LENTEUR': 'FAIBLE',
            'AUTRE': 'MOYENNE',
        }
        self.priorite = mapping_priorite.get(self.type_probleme, 'MOYENNE')

        # 2. Remplissage auto de la description si elle est vide
        if not self.description:
            if self.type_probleme == 'AUTRE':
                self.description = self.suggestions_autre or "Autre problème non listé"
            else:
                # Récupère le texte lisible de l'option choisie
                self.description = dict(self.TYPES_PROBLEMES).get(self.type_probleme)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_ticket} - {self.client}"

    @property
    def respecte_sla(self):
        # Logique pour vérifier si le ticket a été résolu dans les délais impartis [cite: 128]
        # Exemple pour Critique : 2 heures
        limit = self.cree_le + timedelta(hours=2)
        if self.statut == 'RESOLU' and self.date_resolution <= limit:
            return True
        return False
    
class Documentation(models.Model):
    CATEGORIES = [
        ('TECHNIQUE', 'Guide Technique'),
        ('UTILISATEUR', 'Guide Utilisateur'),
        ('PROCEDURE', 'Procédure Interne'),
    ]

    titre = models.CharField(max_length=200) # [cite: 28]
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='TECHNIQUE')
    contenu = models.TextField(help_text="Décrivez ici la solution pas à pas") # [cite: 30]
    cree_le = models.DateTimeField(auto_now_add=True)
    mis_a_jour_le = models.DateTimeField(auto_now=True)
    auteur = models.CharField(max_length=100, default="Aboubacar Sidick") # [cite: 8, 82]

    def __str__(self):
        return f"{self.categorie} - {self.titre}"

    class Meta:
        verbose_name = "Fiche Technique"
        verbose_name_plural = "Base de Connaissances"