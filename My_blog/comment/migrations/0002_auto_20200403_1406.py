# Generated by Django 2.2.10 on 2020-04-03 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
    ]
