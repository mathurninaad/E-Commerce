# Generated by Django 3.2.7 on 2021-10-14 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20211013_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('e_mail', models.CharField(default='', max_length=50)),
                ('message', models.CharField(default='', max_length=300)),
            ],
        ),
    ]
