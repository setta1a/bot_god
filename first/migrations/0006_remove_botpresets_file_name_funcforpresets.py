# Generated by Django 4.1.7 on 2023-05-02 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0005_botpresets_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botpresets',
            name='file_name',
        ),
        migrations.CreateModel(
            name='FuncForPresets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.botpresets')),
                ('func', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.botfunctions')),
            ],
        ),
    ]
