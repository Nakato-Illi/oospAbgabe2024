# Generated by Django 5.0.1 on 2024-01-20 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awamain', '0003_alter_post_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]
