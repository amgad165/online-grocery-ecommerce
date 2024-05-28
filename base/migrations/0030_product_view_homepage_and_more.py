# Generated by Django 5.0.4 on 2024-05-28 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_ingredient_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='view_homepage',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ingredientusercustomize',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='quantity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=355, null=True),
        ),
        migrations.AlterField(
            model_name='productingredient',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='quantity'),
        ),
    ]
