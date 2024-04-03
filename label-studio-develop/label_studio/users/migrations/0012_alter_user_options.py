# Generated by Django 3.2.23 on 2024-03-21 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('project_view_GET', 'view project'), ('project_create_PATCH', 'create project'), ('project_del_DELETE', 'del project'), ('project_edit_PATCH', 'edit project'), ('project_data_import_POST', 'data import project'), ('project_data_export_GET', 'data export project'), ('dm_tasks_del_POST', 'data manager del tasks'), ('dm_annotations_del_POST', 'data manager del annotations'), ('dm_pred_del_POST', 'data manager del predictions'), ('tasks_annotation_submit_POST', 'tasks submit annotation'), ('tasks_annotation_del_DELETE', 'tasks del annotation'), ('tasks_annotation_update_PATCH', 'tasks update annotation')], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
