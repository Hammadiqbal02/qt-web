# Generated by Django 4.1.6 on 2023-02-08 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('owner', 'Owner'), ('operator', 'Operator')], default='operator', max_length=10),
        ),
    ]
