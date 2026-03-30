from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Service, ServiceCategory, PrintingOption, BindingOption, CustomPrintOption
from orders.models import Cart, CartItem
import json

def services_list(request):
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    return render(request, 'services/services_list.html', {'categories': categories})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required
def printing_service(request):
    services = Service.objects.filter(category__category_type='printing', is_active=True)
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        copies = int(request.POST.get('copies', 1))
        color = request.POST.get('color', 'bw')
        page_size = request.POST.get('page_size', 'A4')
        sides = request.POST.get('sides', 'single')
        pages = int(request.POST.get('pages', 1))
        uploaded_file = request.FILES.get('document')
        service = get_object_or_404(Service, pk=service_id)
        try:
            option = PrintingOption.objects.get(service=service, color_type=color, page_size=page_size, sides=sides)
            price_per_copy = option.price_per_page * pages
        except PrintingOption.DoesNotExist:
            price_per_copy = service.base_price
        total_price = price_per_copy * copies
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_config = {'service_type': 'printing', 'copies': copies, 'color': color, 'page_size': page_size, 'sides': sides, 'pages': pages}
        cart_item = CartItem(cart=cart, service=service, quantity=copies, unit_price=price_per_copy, total_price=total_price, configuration=json.dumps(item_config), file_name=uploaded_file.name if uploaded_file else '')
        cart_item.save()
        if uploaded_file:
            cart_item.uploaded_file = uploaded_file
            cart_item.save()
        messages.success(request, 'Printing service added to cart!')
        return redirect('cart')
    return render(request, 'services/printing.html', {'services': services})

@login_required
def binding_service(request):
    services = Service.objects.filter(category__category_type='binding', is_active=True)
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        binding_type = request.POST.get('binding_type', 'spiral')
        quantity = int(request.POST.get('quantity', 1))
        uploaded_file = request.FILES.get('document')
        service = get_object_or_404(Service, pk=service_id)
        try:
            option = BindingOption.objects.get(service=service, binding_type=binding_type)
            unit_price = option.price
        except BindingOption.DoesNotExist:
            unit_price = service.base_price
        total_price = unit_price * quantity
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_config = {'service_type': 'binding', 'binding_type': binding_type, 'quantity': quantity}
        cart_item = CartItem(cart=cart, service=service, quantity=quantity, unit_price=unit_price, total_price=total_price, configuration=json.dumps(item_config), file_name=uploaded_file.name if uploaded_file else '')
        cart_item.save()
        if uploaded_file:
            cart_item.uploaded_file = uploaded_file
            cart_item.save()
        messages.success(request, 'Binding service added to cart!')
        return redirect('cart')
    return render(request, 'services/binding.html', {'services': services})

@login_required
def custom_printing_service(request):
    services = Service.objects.filter(category__category_type='custom', is_active=True)
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        product_type = request.POST.get('product_type', 'tshirt')
        size = request.POST.get('size', 'M')
        quantity = int(request.POST.get('quantity', 1))
        uploaded_file = request.FILES.get('design')
        service = get_object_or_404(Service, pk=service_id)
        try:
            option = CustomPrintOption.objects.get(service=service, product_type=product_type, size=size)
            unit_price = option.price
        except CustomPrintOption.DoesNotExist:
            unit_price = service.base_price
        total_price = unit_price * quantity
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_config = {'service_type': 'custom', 'product_type': product_type, 'size': size, 'quantity': quantity}
        cart_item = CartItem(cart=cart, service=service, quantity=quantity, unit_price=unit_price, total_price=total_price, configuration=json.dumps(item_config), file_name=uploaded_file.name if uploaded_file else '')
        cart_item.save()
        if uploaded_file:
            cart_item.uploaded_file = uploaded_file
            cart_item.save()
        messages.success(request, 'Custom printing added to cart!')
        return redirect('cart')
    return render(request, 'services/custom_printing.html', {'services': services})

def get_price(request):
    service_id = request.GET.get('service_id')
    color = request.GET.get('color', 'bw')
    page_size = request.GET.get('page_size', 'A4')
    sides = request.GET.get('sides', 'single')
    pages = int(request.GET.get('pages', 1))
    copies = int(request.GET.get('copies', 1))
    try:
        option = PrintingOption.objects.get(service_id=service_id, color_type=color, page_size=page_size, sides=sides)
        price_per_copy = float(option.price_per_page) * pages
        total = price_per_copy * copies
        return JsonResponse({'price_per_copy': round(price_per_copy,2), 'total': round(total,2)})
    except PrintingOption.DoesNotExist:
        return JsonResponse({'price_per_copy': 0, 'total': 0})

def get_custom_price(request):
    service_id = request.GET.get('service_id')
    product_type = request.GET.get('product_type')
    size = request.GET.get('size')
    quantity = int(request.GET.get('quantity', 1))
    try:
        option = CustomPrintOption.objects.get(service_id=service_id, product_type=product_type, size=size)
        total = float(option.price) * quantity
        return JsonResponse({'unit_price': float(option.price), 'total': round(total,2)})
    except CustomPrintOption.DoesNotExist:
        return JsonResponse({'unit_price': 0, 'total': 0})
