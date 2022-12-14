# Generated by Django 4.1.1 on 2022-09-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number_id', models.CharField(max_length=23)),
                ('name', models.CharField(max_length=21)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('display_phone_number', models.CharField(max_length=17)),
                ('wa_id', models.CharField(max_length=23)),
                ('incoming_msg', models.CharField(max_length=250)),
                ('gpt_response', models.CharField(max_length=250)),
            ],
        ),
    ]
