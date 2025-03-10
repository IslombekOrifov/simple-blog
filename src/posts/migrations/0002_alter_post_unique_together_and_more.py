# Generated by Django 4.2 on 2023-06-15 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('image', 'body', 'date_created')},
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-date_created', 'slug', 'status'], name='posts_post_date_cr_c1b758_idx'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='publish',
        ),
    ]
