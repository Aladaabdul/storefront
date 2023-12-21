# Generated by Django 4.2.7 on 2023-11-28 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='membership',
            field=models.CharField(choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold')], default='MEMBERSHIP_BRONZE', max_length=50),
        ),
    ]