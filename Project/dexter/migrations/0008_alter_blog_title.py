# Generated by Django 5.1 on 2024-08-24 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dexter', '0007_alter_blog_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=70),
        ),
    ]
