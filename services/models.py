from django.db import models


class ServiceCategory(models.Model):
    CATEGORY_CHOICES = [
        ('printing', 'Printing'),
        ('binding', 'Spiral Binding'),
        ('custom', 'Custom Printing'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='bi-printer')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Service Categories'


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.name


class PrintingOption(models.Model):
    PAGE_SIZE_CHOICES = [
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('Letter', 'Letter'),
        ('Legal', 'Legal'),
    ]
    COLOR_CHOICES = [
        ('bw', 'Black & White'),
        ('color', 'Color'),
    ]
    SIDE_CHOICES = [
        ('single', 'Single Side'),
        ('double', 'Double Side'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='printing_options')
    page_size = models.CharField(max_length=10, choices=PAGE_SIZE_CHOICES, default='A4')
    color_type = models.CharField(max_length=10, choices=COLOR_CHOICES, default='bw')
    sides = models.CharField(max_length=10, choices=SIDE_CHOICES, default='single')
    price_per_page = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.service.name} - {self.page_size} {self.color_type} {self.sides}"


class BindingOption(models.Model):
    BINDING_CHOICES = [
        ('spiral', 'Spiral Binding'),
        ('comb', 'Comb Binding'),
        ('tape', 'Tape Binding'),
        ('hard', 'Hard Cover'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='binding_options')
    binding_type = models.CharField(max_length=20, choices=BINDING_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.service.name} - {self.binding_type}"


class CustomPrintOption(models.Model):
    PRODUCT_CHOICES = [
        ('tshirt', 'T-Shirt'),
        ('mug', 'Mug'),
        ('photo', 'Photo Print'),
        ('poster', 'Poster'),
        ('banner', 'Banner'),
        ('visiting_card', 'Visiting Card'),
    ]
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('XXL', 'XX-Large'),
        ('4x6', '4x6 inch'),
        ('5x7', '5x7 inch'),
        ('8x10', '8x10 inch'),
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('custom', 'Custom Size'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='custom_options')
    product_type = models.CharField(max_length=20, choices=PRODUCT_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.service.name} - {self.product_type} ({self.size})"
