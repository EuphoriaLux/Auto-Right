# Generated by Django 4.2.2 on 2023-09-15 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_requests', '0007_categoryrisk_remove_risk_url_alter_category_risk_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='risk',
            name='categories',
        ),
        migrations.AddField(
            model_name='risk',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='risks', to='company_requests.categoryrisk'),
        ),
    ]