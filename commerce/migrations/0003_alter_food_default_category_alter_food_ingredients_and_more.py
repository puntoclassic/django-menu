# Generated by Django 4.0.4 on 2022-06-22 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_food_price_alter_food_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='default_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='foods', to='commerce.category', verbose_name='Categoria di default'),
        ),
        migrations.AlterField(
            model_name='food',
            name='ingredients',
            field=models.TextField(default='', verbose_name='Ingredienti'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Prezzo'),
        ),
    ]
