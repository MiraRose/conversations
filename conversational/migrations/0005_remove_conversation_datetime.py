# Generated by Django 3.2.4 on 2021-06-10 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversational', '0004_thought'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='datetime',
        ),
    ]