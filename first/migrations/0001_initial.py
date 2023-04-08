from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotFunctions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func_name', models.CharField(max_length=64)),
                ('file_name', models.CharField(max_length=64)),
            ],
        ),
    ]
