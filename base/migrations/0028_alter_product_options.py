# Generated by Django 5.0.4 on 2024-05-27 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_alter_customuser_address_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-customize', 'name']},
        ),
    ]
