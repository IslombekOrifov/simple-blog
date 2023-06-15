# Generated by Django 4.2 on 2023-06-15 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_author_alter_post_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='text',
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('image', 'text', 'date_created')},
        ),
    ]
