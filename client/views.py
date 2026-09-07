import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import ContactMessage, JobApplication, JobOffer, Order


def home(request):
    return render(request, 'client/home.html')


def about(request):
    return render(request, 'client/about.html')


def careers_jobs(request):
    offers = JobOffer.objects.filter(is_active=True)
    return render(request, 'client/careers_jobs.html', {'offers': offers})


def careers_spontaneous(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        position = request.POST.get('position', '').strip()
        cv_link = request.POST.get('cv_link', '').strip()
        message = request.POST.get('message', '').strip()

        offer = None
        offer_id = request.POST.get('offer_id', '').strip()
        if offer_id.isdigit():
            offer = JobOffer.objects.filter(pk=int(offer_id), is_active=True).first()

        if not first_name or not last_name or not email or not phone:
            messages.error(request, 'Merci de renseigner vos nom, prénom, email et téléphone.')
            return render(request, 'client/careers_spontaneous.html', {
                'form_data': {
                    'first_name': first_name, 'last_name': last_name, 'email': email,
                    'phone': phone, 'position': position, 'cv_link': cv_link, 'message': message,
                },
                'offer': offer,
            })

        JobApplication.objects.create(
            offer=offer,
            is_spontaneous=offer is None and not position,
            first_name=first_name, last_name=last_name, email=email, phone=phone,
            position=position or (offer.title if offer else ''),
            cv_link=cv_link, message=message,
        )
        messages.success(request, 'Merci ! Votre candidature a bien été transmise à notre service RH.')
        return redirect('client:careers_spontaneous')

    offer = None
    offer_id = request.GET.get('offer', '').strip()
    if offer_id.isdigit():
        offer = JobOffer.objects.filter(pk=int(offer_id), is_active=True).first()
    prefill = request.GET.get('poste', '').strip()
    return render(request, 'client/careers_spontaneous.html', {
        'offer': offer,
        'form_data': {'position': offer.title if offer else prefill},
    })


def bon_plan(request):
    return render(request, 'client/bon_plan.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, 'Merci de renseigner votre nom, votre email et votre message.')
            return render(request, 'client/contact.html', {
                'form_data': {
                    'name': name, 'email': email, 'phone': phone,
                    'subject': subject, 'message': message,
                },
            })

        ContactMessage.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message,
        )
        messages.success(request, 'Merci ! Votre message a bien été envoyé. Notre équipe vous recontacte rapidement.')
        return redirect('client:contact')

    return render(request, 'client/contact.html')


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


