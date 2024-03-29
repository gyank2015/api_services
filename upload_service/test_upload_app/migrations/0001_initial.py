# Generated by Django 2.0.2 on 2018-06-13 08:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='uploadedImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageHash', models.CharField(default='default', max_length=32)),
                ('imageType', models.CharField(default='image/jpg', max_length=15)),
                ('uploadedBy', models.CharField(default='default', max_length=100)),
                ('uploadedAt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'uploaded_images',
            },
        ),
    ]
