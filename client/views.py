import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Order


def home(request):
    return render(request, 'client/home.html')


def bon_plan(request):
    return render(request, 'client/bon_plan.html')


@require_http_methods(['POST'])
def submit_order(request):
    data = json.loads(request.body.decode('utf-8'))
    order = Order.objects.create(
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        phone=data.get('phone', ''),
        email=data.get('email', ''),
        company=data.get('company', ''),
        address=data.get('address', ''),
        instructions=data.get('instructions', ''),
        delivery_slot=data.get('delivery_slot', ''),
        payment_method=data.get('payment_method', 'tmoney'),
        products=data.get('products', []),
        total_amount=data.get('total_amount', 0),
    )
    return JsonResponse({'redirect_url': reverse('client:confirmation', args=[order.pk])})


def confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    formatted_total = '{:,}'.format(order.total_amount).replace(',', ' ')
    return render(request, 'client/confirmation.html', {'order': order, 'formatted_total': formatted_total})


