# Generated by Django 2.2.5 on 2020-06-11 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reductcontract', '0004_auto_20200610_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractor',
            options={'ordering': ['first_name']},
        ),
    ]
