# Generated by Django 4.2.7 on 2023-12-07 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_customer_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
