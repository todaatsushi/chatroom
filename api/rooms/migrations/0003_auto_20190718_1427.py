# Generated by Django 2.2.3 on 2019-07-18 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20190716_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chatroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='rooms.Chatroom'),
        ),
    ]
