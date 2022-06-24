# Generated by Django 4.0.4 on 2022-06-24 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commerce', '0005_alter_orderstatus_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Cliente',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderStatus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='commerce.orderstatus', verbose_name='Stato ordine'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shippingCosts',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, verbose_name='Costi di consegna'),
        ),
    ]
