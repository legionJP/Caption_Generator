# Generated by Django 5.1.1 on 2024-09-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0002_remove_subtitle_timestamp_subtitle_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitle',
            name='file',
            field=models.FileField(default='subtitles/placeholder.srt', upload_to='subtitles/'),
        ),
    ]
