# Generated by Django 2.0.13 on 2019-08-13 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('first_password', models.CharField(max_length=200)),
                ('second_password', models.CharField(max_length=200)),
            ],
        ),
    ]
