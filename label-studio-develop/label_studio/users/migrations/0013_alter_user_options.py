# Generated by Django 3.2.23 on 2024-03-21 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('projectlist_get', 'projects_view'), ('projectlist_post', 'projects_create'), ('project_get', 'projects_view'), ('project_del', 'projects_delete'), ('project_patch', 'projects_change'), ('project_put', 'projects_change'), ('project_post', 'projects_create')], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
