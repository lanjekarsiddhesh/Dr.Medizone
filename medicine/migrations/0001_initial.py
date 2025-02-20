# Generated by Django 4.0.6 on 2023-01-27 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DMZ', '0002_alter_bill_bill_date_alter_doctor_joining_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Brand_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('total', models.FloatField(default=0)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='DMZ.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('Id', models.BigAutoField(primary_key=True, serialize=False)),
                ('medicine_name', models.CharField(max_length=200)),
                ('medicine_quantity', models.CharField(max_length=200)),
                ('Total_medicines', models.IntegerField()),
                ('price', models.FloatField()),
                ('price_off', models.CharField(max_length=200)),
                ('discription', models.CharField(max_length=1000)),
                ('uses', models.CharField(max_length=500)),
                ('Image1', models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')),
                ('Image2', models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')),
                ('Image3', models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')),
                ('Image4', models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicine.category')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('product_img', models.ImageField(upload_to='medicine_imgs/MedizoneShop/ReviewProduct')),
                ('subject', models.CharField(default='', max_length=500)),
                ('review', models.TextField(blank=True, max_length=5000)),
                ('rating', models.FloatField()),
                ('created_Time_at', models.TimeField(auto_now_add=True)),
                ('created_Date_at', models.DateField(auto_now_add=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DMZ.patient')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicine.products')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('Orders_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('signature', models.CharField(max_length=500, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('Date', models.DateField(auto_now_add=True)),
                ('Time', models.TimeField(auto_now_add=True)),
                ('Cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='medicine.cart')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('order', models.CharField(max_length=500, null=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='medicine.products')),
                ('carts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carItems', to='medicine.cart')),
            ],
        ),
    ]
