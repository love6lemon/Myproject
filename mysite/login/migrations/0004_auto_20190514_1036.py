# Generated by Django 2.2 on 2019-05-14 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20190508_1502'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='User1',
        ),
        migrations.AlterModelOptions(
            name='user1',
            options={'ordering': ['-c_time'], 'verbose_name': '用户1', 'verbose_name_plural': '用户1'},
        ),
        migrations.AddField(
            model_name='asset',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='login.User1', verbose_name='唯一用户名'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin', to=settings.AUTH_USER_MODEL, verbose_name='资产管理员'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by', to=settings.AUTH_USER_MODEL, verbose_name='批准人'),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='事件执行人'),
        ),
    ]
