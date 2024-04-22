"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging   # noqa: I001
from typing import Optional

from rest_framework.permissions import BasePermission
from pydantic import BaseModel

import rules

logger = logging.getLogger(__name__)


class AllPermissions(BaseModel):
    organizations_create = 'organizations.create'
    organizations_view = 'organizations.view'
    organizations_change = 'organizations.change'
    organizations_delete = 'organizations.delete'
    organizations_invite = 'organizations.invite'
    projects_create = 'projects.create'
    projects_view = 'projects.view'
    projects_change = 'projects.change'
    projects_delete = 'projects.delete'
    tasks_create = 'tasks.create'
    tasks_view = 'tasks.view'
    tasks_change = 'tasks.change'
    tasks_delete = 'tasks.delete'
    annotations_create = 'annotations.create'
    annotations_view = 'annotations.view'
    annotations_change = 'annotations.change'
    annotations_delete = 'annotations.delete'
    actions_perform = 'actions.perform'
    predictions_any = 'predictions.any'
    avatar_any = 'avatar.any'
    labels_create = 'labels.create'
    labels_view = 'labels.view'
    labels_change = 'labels.change'
    labels_delete = 'labels.delete'
    models_create = 'models.create'
    models_view = 'models.view'
    models_change = 'models.change'
    models_delete = 'models.delete'
    model_provider_connection_create = 'model_provider_connection.create'
    model_provider_connection_view = 'model_provider_connection.view'
    model_provider_connection_change = 'model_provider_connection.change'
    model_provider_connection_delete = 'model_provider_connection.delete'



all_permissions = AllPermissions()


class ViewClassPermission(BaseModel):
    GET: Optional[str] = None
    PATCH: Optional[str] = None
    PUT: Optional[str] = None
    DELETE: Optional[str] = None
    POST: Optional[str] = None


def make_perm(name, pred, overwrite=False):
    if rules.perm_exists(name):
        if overwrite:
            rules.remove_perm(name)
        else:
            return
    rules.add_perm(name, pred)


for _, permission_name in all_permissions:
    make_perm(permission_name, rules.is_authenticated)

class ProjectListPermission(BasePermission):
    message = "用户无权限 ProjectListPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'GET':
            if request.user.has_perm('users.projects_projectlist_get'):
                return True
        if request.method == 'POST':
            ##要禁止创建项目必须禁止该projectlist_post选项
            if request.user.has_perm('users.projects_projectlist_post'):
                return True
        return False
    
class ProjectPermission(BasePermission):
    message = "用户无权限 ProjectPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        # 这里的逻辑仅适用于基于对象的动作，如 retrieve, update, destroy
        if request.method == 'GET':
            if request.user.has_perm('users.projects_project_get'):
                return True
        if request.method == 'PUT':
            if request.user.has_perm('users.projects_project_put'):
                return True
        if request.method == 'DELETE':
            if request.user.has_perm('users.projects_project_del'):
                return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.projects_project_patch'):
                return True
        if request.method == 'POST':
            if request.user.has_perm('users.projects_project_post'):
                return True
        return False
    
class ProjectTaskListPermission(BasePermission):
    message = "用户无权限 ProjectTaskListPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        # 这里的逻辑仅适用于基于对象的动作，如 retrieve, update, destroy
        if request.method == 'GET':
            if request.user.has_perm('users.projects_projecttasklist_get'):
                return True
        if request.method == 'DELETE':
            if request.user.has_perm('users.projects_projecttasklist_del'):
                return True
        if request.method == 'POST':
            if request.user.has_perm('users.projects_projecttasklist_post'):
                return True
        return False    
    
class ProjectimportPermission(BasePermission):
    message = "用户无权限 ProjectimportPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'POST':
            if request.user.has_perm('users.data_import_post'):
                return True
        return False
    
class ProjectexportPermission(BasePermission):
    message = "用户无权限 ProjectexportPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        # 这里的逻辑仅适用于基于对象的动作，如 retrieve, update, destroy
        if request.method == 'GET':
            if request.user.has_perm('users.data_export_get'):
                return True
        return False

class dataactionPermission(BasePermission):
    message = "用户无权限 dataactionPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        #view project inner tasks
        if request.method == 'GET':
            if request.user.has_perm('users.data_manager_action_get'):
                return True
         #charge project inner tasks
        if request.method == 'POST':
            if request.user.has_perm('users.data_manager_action_post'):
                return True
        return False

class dataviewPermission(BasePermission):
    message = "用户无权限 dataviewPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'GET':
            if request.user.has_perm('users.data_manager_view_get'):
                return True
        if request.method == 'PUT':
            if request.user.has_perm('users.data_manager_view_put'):
                return True
        if request.method == 'DELETE':
                return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.data_manager_view_patch'):
                return True
        if request.method == 'POST':
            if request.user.has_perm('users.data_manager_view_post'):
                return True
        return False
    def has_object_permission(self, request, view, obj):
        if obj.user==request.user or request.user.has_perm('users.data_manager_view_super'):
            return True
        return False

class mlPermission(BasePermission):
    message = "用户无权限 mlPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'DELETE':
            if request.user.has_perm('users.ml_del'):
                return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.ml_patch'):
                return True
        if request.method == 'POST':
            if request.user.has_perm('users.ml_post'):
                return True
        if request.method == 'GET':
            return True
        return False

class TaskListPermission(BasePermission):
    message = "用户无权限 TaskListPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'GET':
            if request.user.has_perm('users.tasks_taskslist_get'):
                return True
        if request.method == 'POST':
            ##要禁止创建项目必须禁止该projectlist_post选项
            if request.user.has_perm('users.tasks_taskslist_post'):
                return True
        return False

class TaskPermission(BasePermission):
    message = "用户无权限 TaskPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        # 这里的逻辑仅适用于基于对象的动作，如 retrieve, update, destroy
        if request.method == 'GET':
            if request.user.has_perm('users.tasks_get'):
                return True
        if request.method == 'PUT':
            if request.user.has_perm('users.tasks_put'):
                return True
        if request.method == 'DELETE':
            if request.user.has_perm('users.tasks_delete'):
                return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.tasks_patch'):
                return True
        return False

class annotationlistPermission(BasePermission):
    message = "用户无权限 annotationlistPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'GET':
            if request.user.has_perm('users.tasks_annotationlist_get'):
                return True
        if request.method == 'POST':
            ##要禁止创建项目必须禁止该projectlist_post选项
            if request.user.has_perm('users.tasks_annotationlist_post'):
                return True
        return False    

class annotationsPermission(BasePermission):
    message = "用户无权限 annotationsPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        #view project inner tasks
        if request.method == 'GET':
            if request.user.has_perm('users.tasks_annotations_get'):
                return True
         #charge project inner tasks
        if request.method == 'PUT':
            if request.user.has_perm('users.tasks_annotations_put'):
                return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.tasks_annotations_patch'):
                return True
        if request.method == 'DELETE':
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.completed_by==request.user or request.user.has_perm('users.tasks_annotations_super'):
            return True
        return False

class censorPermission(BasePermission):
    message = "用户无权限 censorPermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.tasks_annotations_super'):
                return True
        return False
    
class iostorePermission(BasePermission):
    message = "用户无权限 iostorePermission" 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method == 'PATCH':
            if request.user.has_perm('users.iostore_super'):
                return True
        if request.method == 'GET':
            if request.user.has_perm('users.iostore_super'):
                return True
        if request.method == 'DELETE':
            if request.user.has_perm('users.iostore_super'):
                return True
        if request.method == 'POST':
            if request.user.has_perm('users.iostore_super'):
                return True
        return False



    