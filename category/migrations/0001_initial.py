# Generated by Django 4.2.4 on 2023-08-07 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('category_online', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/categories')),
                ('gender', models.CharField(choices=[('H', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], default='', max_length=1)),
                ('product_type', models.CharField(choices=[('Y', 'Accessoires Homme'), ('X', 'Accessoires Femme'), ('A', 'Vêtements Homme'), ('B', 'Vêtements Femme'), ('O', 'Autre')], default='', max_length=1)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]
