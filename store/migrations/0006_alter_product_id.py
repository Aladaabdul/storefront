# Generated by Django 4.2.2 on 2023-08-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_collection_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
