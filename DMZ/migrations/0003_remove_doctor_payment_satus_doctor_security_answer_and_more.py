# Generated by Django 4.0.6 on 2023-01-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DMZ', '0002_alter_bill_bill_date_alter_doctor_joining_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='payment_satus',
        ),
        migrations.AddField(
            model_name='doctor',
            name='Security_Answer',
            field=models.CharField(default='Drmedizone', max_length=500),
        ),
        migrations.AddField(
            model_name='doctor',
            name='Security_Question',
            field=models.CharField(default='What is your name ?', max_length=500),
        ),
        migrations.AddField(
            model_name='doctor',
            name='doctor_college',
            field=models.CharField(default='Mumbai AIMS college', max_length=200),
        ),
        migrations.AddField(
            model_name='doctor',
            name='year_of_compilation',
            field=models.CharField(default='1995', max_length=200),
        ),
    ]
