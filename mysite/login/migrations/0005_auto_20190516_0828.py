# Generated by Django 2.2 on 2019-05-16 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20190514_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='newassetapprovalzone',
            name='user1',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='资产所有者'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='login.User1', verbose_name='所有者'),
        ),
    ]
