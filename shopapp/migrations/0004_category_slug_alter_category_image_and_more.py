# Generated by Django 4.0.4 on 2022-05-09 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0003_alter_category_active_alter_manufacturer_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', editable=False, verbose_name='Permalink'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='public/assets/images/c', verbose_name='Immagine categoria'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='public/assets/images/m', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='imageUrl',
            field=models.URLField(blank=True, null=True, verbose_name='URL Logo scaricabile'),
        ),
    ]
