# Generated by Django 3.2.4 on 2021-06-10 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversational', '0009_alter_conversation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='date',
            field=models.DateField(default=datetime.date(2021, 6, 10)),
        ),
    ]