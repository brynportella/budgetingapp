# Generated by Django 3.1 on 2020-09-13 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goaltype',
            name='goal_category',
            field=models.CharField(choices=[('SAVING', 'Saving'), ('PAYING_DOWN_DEBT', 'Paying Down Debt'), ('INVESTING', 'Investing')], default='SAVING', max_length=100),
            preserve_default=False,
        ),
    ]