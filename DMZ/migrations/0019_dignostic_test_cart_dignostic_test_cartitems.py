# Generated by Django 4.0.6 on 2023-04-08 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DMZ', '0018_diagnostic_test_list_home_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='dignostic_test_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lab_cart', to='DMZ.patient')),
            ],
        ),
        migrations.CreateModel(
            name='dignostic_test_cartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=500, null=True)),
                ('Tests', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lab_tests', to='DMZ.diagnostic_test_list')),
                ('carts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lab_carItems', to='DMZ.dignostic_test_cart')),
            ],
        ),
    ]
