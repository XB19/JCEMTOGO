from django import forms

from client.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'company',
            'address',
            'delivery_slot',
            'payment_method',
            'instructions',
            'total_amount',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'input-field'}),
            'phone': forms.TextInput(attrs={'placeholder': '+228 ...', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': 'client@exemple.com', 'class': 'input-field'}),
            'company': forms.TextInput(attrs={'placeholder': 'Nom de l’entreprise (optionnel)', 'class': 'input-field'}),
            'address': forms.Textarea(attrs={'placeholder': 'Adresse de livraison', 'rows': 2, 'class': 'input-field'}),
            'delivery_slot': forms.TextInput(attrs={'placeholder': 'Ex. 10h-12h', 'class': 'input-field'}),
            'payment_method': forms.Select(attrs={'class': 'input-field'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Notes et consignes', 'rows': 3, 'class': 'input-field'}),
            'total_amount': forms.NumberInput(attrs={'placeholder': 'Montant en FCFA', 'class': 'input-field'}),
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'phone': 'Téléphone',
            'email': 'Email',
            'company': 'Société',
            'address': 'Adresse',
            'delivery_slot': 'Créneau de livraison',
            'payment_method': 'Méthode de paiement',
            'instructions': 'Instructions de livraison',
            'total_amount': 'Montant total (FCFA)',
        }
