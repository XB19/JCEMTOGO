from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from client.models import Order
from .forms import OrderForm


def dashboard(request):
    all_orders = Order.objects.order_by('-created_at')
    recent_orders = all_orders[:5]
    stats = {
        'today_orders': all_orders.count(),
        'total_revenue': sum(o.total_amount for o in all_orders),
        'in_route': all_orders.filter(status='delivering').count(),
        'delivered': all_orders.filter(status='delivered').count(),
    }
    return render(
        request,
        'backoffice/dashboard.html',
        {
            'orders': recent_orders,
            'stats': stats,
            'active': 'dashboard',
            'create_url': '/back-office/new-order/',
            'status_choices': Order.STATUS_CHOICES,
        },
    )


def orders(request):
    order_list = Order.objects.order_by('-created_at')[:50]
    stats = {
        'total': Order.objects.count(),
        'pending': Order.objects.filter(status='pending').count(),
        'delivering': Order.objects.filter(status='delivering').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
    }
    return render(
        request,
        'backoffice/orders.html',
        {
            'title': 'Commandes',
            'orders': order_list,
            'stats': stats,
            'active': 'orders',
            'create_url': '/back-office/new-order/',
            'status_choices': Order.STATUS_CHOICES,
        },
    )


@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('status')
    valid_statuses = dict(Order.STATUS_CHOICES)
    if new_status in valid_statuses:
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        messages.success(
            request,
            f"Commande {order.order_reference} : statut mis à jour vers « {valid_statuses[new_status]} ».",
        )
    else:
        messages.error(request, "Statut invalide.")
    next_url = request.POST.get('next') or reverse('backoffice:orders')
    return redirect(next_url)


def deliveries(request):
    delivery_orders = Order.objects.exclude(status='pending').order_by('-created_at')
    stats = {
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'preparing': Order.objects.filter(status='preparing').count(),
        'delivering': Order.objects.filter(status='delivering').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
    }
    return render(
        request,
        'backoffice/deliveries.html',
        {
            'orders': delivery_orders,
            'stats': stats,
            'active': 'deliveries',
            'status_choices': Order.STATUS_CHOICES,
        },
    )


def planning(request):
    active_orders = Order.objects.exclude(status__in=['delivered', 'cancelled']).order_by('delivery_slot', '-created_at')
    slots = {}
    for order in active_orders:
        key = order.delivery_slot or 'Créneau non défini'
        slots.setdefault(key, []).append(order)
    return render(
        request,
        'backoffice/planning.html',
        {
            'slots': slots,
            'active': 'planning',
            'status_choices': Order.STATUS_CHOICES,
        },
    )


def trucks(request):
    return render(
        request,
        'backoffice/page_placeholder.html',
        {
            'title': 'Camions',
            'description': "Aucun camion enregistré pour l'instant. Cette section affichera la flotte, les affectations de chauffeurs et la disponibilité des véhicules dès que le module sera activé.",
            'active': 'trucks',
        },
    )


def billing(request):
    order_list = Order.objects.order_by('-created_at')
    total_revenue = sum(o.total_amount for o in order_list)
    by_method = []
    for value, label in Order.PAYMENT_METHOD_CHOICES:
        amount = order_list.filter(payment_method=value).aggregate(total=Sum('total_amount'))['total'] or 0
        by_method.append({'label': label, 'amount': amount})
    return render(
        request,
        'backoffice/billing.html',
        {
            'orders': order_list[:50],
            'total_revenue': total_revenue,
            'by_method': by_method,
            'active': 'billing',
        },
    )


def reports(request):
    order_list = Order.objects.all()
    total_orders = order_list.count()
    total_revenue = sum(o.total_amount for o in order_list)
    avg_order = round(total_revenue / total_orders) if total_orders else 0
    status_breakdown = [
        {'value': value, 'label': label, 'count': order_list.filter(status=value).count()}
        for value, label in Order.STATUS_CHOICES
    ]
    payment_breakdown = [
        {'label': label, 'count': order_list.filter(payment_method=value).count()}
        for value, label in Order.PAYMENT_METHOD_CHOICES
    ]
    return render(
        request,
        'backoffice/reports.html',
        {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'avg_order': avg_order,
            'status_breakdown': status_breakdown,
            'payment_breakdown': payment_breakdown,
            'active': 'reports',
        },
    )


def new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'pending'
            order.save()
            messages.success(request, 'La commande a été enregistrée avec succès.')
            return redirect('backoffice:orders')
    else:
        form = OrderForm()

    return render(
        request,
        'backoffice/new_order.html',
        {'form': form, 'active': 'orders'},
    )
