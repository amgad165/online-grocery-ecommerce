# Generated by Django 5.0.4 on 2024-05-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_alter_transaction_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_period',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
