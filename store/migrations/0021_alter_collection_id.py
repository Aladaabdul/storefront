# Generated by Django 4.2.7 on 2023-12-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_collection_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
