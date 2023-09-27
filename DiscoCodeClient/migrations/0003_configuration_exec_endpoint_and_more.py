# Generated by Django 4.2.4 on 2023-09-27 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiscoCodeClient', '0002_configuration_alt_prefix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='exec_endpoint',
            field=models.CharField(default='https://emkc.org/api/v2/piston/execute', max_length=255, null=True, verbose_name='Code Execution Endpoint'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='runtime_endpoint',
            field=models.CharField(default='https://emkc.org/api/v2/piston/runtimes', max_length=255, null=True, verbose_name='Query Runtime Endpoint'),
        ),
    ]