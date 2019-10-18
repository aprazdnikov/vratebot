# Generated by Django 2.2.6 on 2019-10-18 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ImageField(upload_to='')),
                ('user_name', models.CharField(max_length=255)),
                ('btc_balance', models.FloatField()),
                ('eth_balance', models.FloatField()),
            ],
        ),
    ]
