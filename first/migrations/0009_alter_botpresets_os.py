# Generated by Django 4.2 on 2023-05-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0008_botpresets_os'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botpresets',
            name='os',
            field=models.CharField(max_length=10),
        ),
    ]
