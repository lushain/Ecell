# Generated by Django 5.1 on 2024-08-24 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dexter', '0004_remove_userinvention_desc_remove_userinvention_img_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invention',
        ),
        migrations.DeleteModel(
            name='UserInvention',
        ),
    ]
