# Generated by Django 3.2.25 on 2025-01-06 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VoteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house', models.CharField(choices=[('l', 'Lyceum'), ('p', 'Parnassus'), ('v', 'Virtus')], max_length=1, verbose_name='House')),
                ('visitor_ip', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name='Visitor IP')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='Last modified time')),
            ],
            options={
                'verbose_name': 'Vote Data',
                'verbose_name_plural': 'Vote Data',
                'ordering': ['-creation_time'],
            },
        ),
    ]
