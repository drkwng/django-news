# Generated by Django 3.2.9 on 2021-12-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_comment_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_moderated',
            field=models.BooleanField(default=False),
        ),
    ]
