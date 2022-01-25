# Generated by Django 4.0 on 2022-01-23 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_uploadi̇mg_imgname'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docname', models.FileField(upload_to='ximages')),
                ('size', models.CharField(default='', max_length=10)),
                ('doccode', models.TextField()),
                ('username', models.CharField(default='', max_length=80)),
                ('userid', models.CharField(default='', max_length=5)),
                ('keyid', models.CharField(default='', max_length=5)),
            ],
        ),
        migrations.AlterField(
            model_name='uploadi̇mg',
            name='imgname',
            field=models.ImageField(upload_to='ximages'),
        ),
    ]
