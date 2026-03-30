from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        return sum(item.total_price for item in self.items.all())

    def get_item_count(self):
        return self.items.count()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    configuration = models.TextField(default='{}')  # JSON string
    uploaded_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} x{self.quantity}"

    def get_config(self):
        import json
        try:
            return json.loads(self.configuration)
        except:
            return {}


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Debit/Credit Card'),
        ('netbanking', 'Net Banking'),
        ('cod', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='upi')
    payment_status = models.CharField(max_length=20, default='paid')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number}"

    class Meta:
        ordering = ['-created_at']

    def get_status_color(self):
        colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'processing': 'primary',
            'ready': 'success',
            'completed': 'success',
            'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')

    def get_status_percent(self):
        percents = {
            'pending': 20,
            'confirmed': 40,
            'processing': 60,
            'ready': 80,
            'completed': 100,
            'cancelled': 0,
        }
        return percents.get(self.status, 0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    configuration = models.TextField(default='{}')
    uploaded_file = models.FileField(upload_to='order_files/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.service.name} in Order #{self.order.order_number}"

    def get_config(self):
        import json
        try:
            return json.loads(self.configuration)
        except:
            return {}
