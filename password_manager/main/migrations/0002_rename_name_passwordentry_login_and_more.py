# Generated by Django 5.0.1 on 2024-01-07 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passwordentry',
            old_name='name',
            new_name='login',
        ),
        migrations.AddField(
            model_name='passwordentry',
            name='service',
            field=models.CharField(default='defauly', max_length=100),
            preserve_default=False,
        ),
    ]