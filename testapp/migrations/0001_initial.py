# Generated by Django 4.1.2 on 2022-11-30 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=90)),
                ('email', models.EmailField(max_length=254)),
                ('pass1', models.CharField(max_length=10)),
                ('pass2', models.CharField(max_length=10)),
            ],
        ),
    ]
