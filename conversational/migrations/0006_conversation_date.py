# Generated by Django 3.2.4 on 2021-06-10 20:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversational', '0005_remove_conversation_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='date',
            field=models.DateField(default=datetime.date(2021, 6, 10)),
        ),
    ]
