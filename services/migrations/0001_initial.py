from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('category_type', models.CharField(
                    choices=[('printing', 'Printing'), ('binding', 'Spiral Binding'), ('custom', 'Custom Printing')],
                    max_length=20,
                )),
                ('description', models.TextField()),
                ('icon', models.CharField(default='bi-printer', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name_plural': 'Service Categories'},
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='services',
                    to='services.servicecategory',
                )),
            ],
        ),
        migrations.CreateModel(
            name='PrintingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_size', models.CharField(
                    choices=[('A4','A4'),('A3','A3'),('Letter','Letter'),('Legal','Legal')],
                    default='A4', max_length=10,
                )),
                ('color_type', models.CharField(
                    choices=[('bw','Black & White'),('color','Color')],
                    default='bw', max_length=10,
                )),
                ('sides', models.CharField(
                    choices=[('single','Single Side'),('double','Double Side')],
                    default='single', max_length=10,
                )),
                ('price_per_page', models.DecimalField(decimal_places=2, max_digits=6)),
                ('service', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='printing_options',
                    to='services.service',
                )),
            ],
        ),
        migrations.CreateModel(
            name='BindingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binding_type', models.CharField(
                    choices=[('spiral','Spiral Binding'),('comb','Comb Binding'),('tape','Tape Binding'),('hard','Hard Cover')],
                    max_length=20,
                )),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('service', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='binding_options',
                    to='services.service',
                )),
            ],
        ),
        migrations.CreateModel(
            name='CustomPrintOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(
                    choices=[('tshirt','T-Shirt'),('mug','Mug'),('photo','Photo Print'),('poster','Poster'),('banner','Banner'),('visiting_card','Visiting Card')],
                    max_length=20,
                )),
                ('size', models.CharField(
                    choices=[('S','Small'),('M','Medium'),('L','Large'),('XL','X-Large'),('XXL','XX-Large'),('4x6','4x6 inch'),('5x7','5x7 inch'),('8x10','8x10 inch'),('A4','A4'),('A3','A3'),('custom','Custom Size')],
                    max_length=10,
                )),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('service', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='custom_options',
                    to='services.service',
                )),
            ],
        ),
    ]
