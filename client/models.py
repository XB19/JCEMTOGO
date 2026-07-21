from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bpe', 'Béton Prêt à l’Emploi'),
        ('mortier', 'Mortier'),
        ('agregat', 'Agrégat'),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='bpe')
    price = models.PositiveIntegerField(help_text='Prix en FCFA par unité ou m³')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('preparing', 'En préparation'),
        ('delivering', 'En livraison'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('tmoney', 'Mixx by Yas'),
        ('flooz', 'Flooz'),
        ('card', 'Carte bancaire'),
        ('cash', 'Espèces'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=24)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    instructions = models.TextField(blank=True)
    delivery_slot = models.CharField(max_length=80)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    products = models.JSONField(default=list)
    total_amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return f"Commande {self.order_reference} — {self.first_name} {self.last_name}"

    @property
    def order_reference(self):
        return f"JCM-{self.pk:06d}" if self.pk else 'JCM-000000'
