# Generated by Django 4.2.4 on 2023-08-28 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scribe_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdfs/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('generated_hpi', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
