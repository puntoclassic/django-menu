# Generated by Django 4.0.4 on 2022-05-16 11:57

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcecatManufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('icecat_id', models.IntegerField()),
                ('logo_url', models.URLField(blank=True, null=True)),
                ('shop_manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marche_icecat', to='commerce.manufacturer', verbose_name='Corrispondenza marca Negozio')),
            ],
            options={
                'verbose_name': 'marca Icecat',
                'verbose_name_plural': 'marche Icecat',
            },
        ),
        migrations.CreateModel(
            name='IcecatCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icecat_id', models.IntegerField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='icecat.icecatcategory', verbose_name='Categoria padre')),
                ('shop_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categorie_icecat', to='commerce.category')),
            ],
            options={
                'verbose_name': 'categoria Icecat',
                'verbose_name_plural': 'categorie Icecat',
            },
        ),
    ]
