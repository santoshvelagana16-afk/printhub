from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
import random, string, os
from .models import Cart, CartItem, Order, OrderItem


def generate_order_number():
    return 'PH' + ''.join(random.choices(string.digits, k=8))


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('service').all()
    return render(request, 'orders/cart.html', {'cart': cart, 'items': items})


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    if not items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    subtotal = cart.get_total()
    tax = subtotal * 18 / 100
    total = subtotal + tax
    return render(request, 'orders/checkout.html', {
        'cart': cart, 'items': items,
        'subtotal': subtotal, 'tax': tax, 'total': total
    })


@login_required
def payment_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    if not items.exists():
        return redirect('cart')
    subtotal = cart.get_total()
    tax = subtotal * 18 / 100
    total = subtotal + tax

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'upi')
        delivery_address = request.POST.get('delivery_address', '')
        notes = request.POST.get('notes', '')

        order = Order.objects.create(
            user=request.user,
            order_number=generate_order_number(),
            status='confirmed',
            payment_method=payment_method,
            payment_status='paid',
            subtotal=subtotal,
            tax=tax,
            total_amount=total,
            delivery_address=delivery_address,
            notes=notes
        )

        for item in items:
            order_item = OrderItem(
                order=order,
                service=item.service,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
                configuration=item.configuration,
                file_name=item.file_name,
            )
            # ── Copy uploaded file from CartItem → OrderItem ──
            if item.uploaded_file:
                try:
                    item.uploaded_file.open('rb')
                    file_content = item.uploaded_file.read()
                    item.uploaded_file.close()
                    fname = os.path.basename(item.uploaded_file.name)
                    order_item.uploaded_file.save(fname, ContentFile(file_content), save=False)
                except Exception:
                    pass
            order_item.save()

        cart.items.all().delete()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'orders/payment.html', {
        'cart': cart, 'items': items,
        'subtotal': subtotal, 'tax': tax, 'total': total
    })


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_tracking(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/tracking.html', {'order': order})
