# Generated by Django 4.2.2 on 2023-09-13 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_requests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('desscription', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='risk',
            field=models.ManyToManyField(blank=True, related_name='categories', to='company_requests.risk'),
        ),
    ]
