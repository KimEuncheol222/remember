# Generated by Django 4.2.5 on 2023-10-05 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0006_alter_post_refreshed_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='user',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]
