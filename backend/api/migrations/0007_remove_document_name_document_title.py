# Generated by Django 5.2.3 on 2025-07-01 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_document_user_documents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='name',
        ),
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default='default_title', max_length=255),
        ),
    ]
