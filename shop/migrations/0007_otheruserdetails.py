# Generated by Django 3.2.7 on 2021-10-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_colour'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherUserDetails',
            fields=[
                ('email', models.CharField(max_length=60, primary_key=True, serialize=False, unique=True)),
                ('mobile', models.CharField(max_length=11)),
                ('age', models.IntegerField(default=13)),
            ],
        ),
    ]
