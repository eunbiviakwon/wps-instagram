# Generated by Django 2.2.9 on 2020-01-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200107_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='태그명')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='posts.Tag', verbose_name='해시태그 목록'),
        ),
    ]
