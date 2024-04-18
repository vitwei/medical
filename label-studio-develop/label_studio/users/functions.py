"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import os
import uuid
from time import time

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.utils.common import load_func
from django import forms
from django.conf import settings
from django.contrib import auth
from django.core.files.images import get_image_dimensions
from django.shortcuts import redirect
from django.urls import reverse
from organizations.models import Organization
import users 
from django.http import JsonResponse


def hash_upload(instance, filename):
    filename = str(uuid.uuid4())[0:8] + '-' + filename
    return settings.AVATAR_PATH + '/' + filename


def check_avatar(files):
    images = list(files.items())
    if not images:
        return None

    _, avatar = list(files.items())[0]  # get first file
    w, h = get_image_dimensions(avatar)
    if not w or not h:
        raise forms.ValidationError("Can't read image, try another one")

    # validate dimensions
    max_width = max_height = 1200
    if w > max_width or h > max_height:
        raise forms.ValidationError('Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))

    valid_extensions = ['jpeg', 'jpg', 'gif', 'png']

    filename = avatar.name
    # check file extension
    ext = os.path.splitext(filename)[1].lstrip('.').lower()
    if ext not in valid_extensions:
        raise forms.ValidationError('Please upload a valid image file with extensions: JPEG, JPG, GIF, or PNG.')

    # validate content type
    main, sub = avatar.content_type.split('/')
    if not (main == 'image' and sub.lower() in valid_extensions):
        raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')

    # validate file size
    max_size = 1024 * 1024
    if len(avatar) > max_size:
        raise forms.ValidationError('Avatar file size may not exceed ' + str(max_size / 1024) + ' kb')

    return avatar


def save_user(request, next_page, user_form):
    """Save user instance to DB"""
    user = user_form.save()
    user.username = user.email.split('@')[0]
    user.save()

    if Organization.objects.exists():
        org = Organization.objects.first()
        org.add_user(user)
    else:
        org = Organization.create_organization(created_by=user, title='Label Studio')
    user.active_organization = org
    user.save(update_fields=['active_organization'])

    request.advanced_json = {
        'email': user.email,
        'allow_newsletters': user.allow_newsletters,
        'update-notifications': 1,
        'new-user': 1,
    }
    redirect_url = next_page if next_page else reverse('projects:project-index')
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(redirect_url)


def proceed_registration(request, user_form, organization_form, next_page):
    """Register a new user for POST user_signup"""
    # save user to db
    save_user = load_func(settings.SAVE_USER)
    response = save_user(request, next_page, user_form)

    return response


def login(request, *args, **kwargs):
    request.session['last_login'] = time()
    return auth.login(request, *args, **kwargs)

def VIT_base_save_user(request, next_page, user_form):
    """Save user instance to DB"""
    user = user_form.save()
    user.username = user.email.split('@')[0]
    user.save()

    if Organization.objects.exists():
        org = Organization.objects.get(title='TempOrganization')
        org.add_user(user)
    else:
        org = Organization.create_organization(created_by=user, title='TempOrganization')
    user.active_organization = org
    user.save(update_fields=['active_organization'])

    request.advanced_json = {
        'email': user.email,
        'allow_newsletters': user.allow_newsletters,
        'update-notifications': 1,
        'new-user': 1,
    }
    redirect_url = next_page if next_page else reverse('projects:project-index')
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(redirect_url)

def VIT_base_proceed_registration(request, user_form, organization_form, next_page):
    """Register a new user for POST user_signup"""
    # save user to db
    response = VIT_base_save_user(request, next_page, user_form)
    return response

def VIT_super_save_user(request, next_page, user_form):
    
    
    """Save super user instance to DB"""
    user = user_form.save()
    user.username = user.email.split('@')[0]
    user.save()

    if Organization.objects.exists():
        org = Organization.objects.get(title='SuperOrganization')
        org.add_user(user)
    else:
        org = Organization.create_organization(created_by=user, title='SuperOrganization')
    user.active_organization = org
    user.save(update_fields=['active_organization'])

    request.advanced_json = {
        'email': user.email,
        'allow_newsletters': user.allow_newsletters,
        'update-notifications': 1,
        'new-user': 1,
    }
    redirect_url = next_page if next_page else reverse('projects:project-index')
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(redirect_url)

def VIT_super_proceed_registration(request, user_form, organization_form, next_page):
    """Register a new user for POST user_signup"""
    # save user to db
    response = VIT_super_save_user(request, next_page, user_form)
    return response

def VIT_super_add_userorg(request,user_form, organization_form, next_page):
    """Save super user instance to DB"""
    adduser=users.models.User.object.get(email=str(user_form.email))
    addorg=Organization.objects.get(title=str(organization_form.title))
    delorg=Organization.objects.get(title=str(adduser.active_organization.title))
    if addorg and adduser and delorg:
        delorg.remove_user(adduser)
        addorg.add_user(adduser)
        adduser.active_organization = addorg
        adduser.save(update_fields=['active_organization'])
        return JsonResponse({'message': 'Operation success'})
    return JsonResponse({'message': 'Operation failed'}, status=400)

def VIT_super_proceed_useraddorg(request,user_form, organization_form, next_page):
    """Register a new user for POST user_signup"""
    # save user to db
    response = VIT_super_add_userorg(request,user_form, organization_form, next_page)
    return response

def VIT_super_del_userorg(request,user_form, organization_form, next_page):
    """Save super user instance to DB"""
    adduser=users.models.User.object.get(email=str(user_form.email))
    addorg=Organization.objects.get(title='TempOrganization')
    delorg=Organization.objects.get(title=str(adduser.active_organization.title))
    if adduser and addorg and delorg and adduser!= delorg:
        delorg.remove_user(adduser)
        addorg.add_user(adduser)
        adduser.active_organization = addorg
        adduser.save(update_fields=['active_organization'])
        return JsonResponse({'message': 'Operation success'})
    return JsonResponse({'message': 'Operation failed'}, status=400)

def VIT_super_proceed_userdelorg(request,user_form, organization_form, next_page):
    """Register a new user for POST user_signup"""
    # save user to db
    response = VIT_super_del_userorg(request,user_form, organization_form, next_page)
    return response


def VIT_addpermission(useremail,permissionname):
    try:
        user=users.models.User.objects.get(email=useremail)
        if not user.has_perm('users.'+permissionname):
            content_type = ContentType.objects.get_for_model(users.models.User)
            permission = Permission.objects.get(
            codename=str(permissionname),
            content_type=content_type,
)
            user.user_permissions.add(permission)
            user=users.models.User.objects.get(email=useremail)
            if user.has_perm('users.'+permissionname):
                return 'OK'
            else:
                return 'Error'
        return 'OK'
    except:
        return "Error please check permissionname"
    
def VIT_delpermission(useremail,permissionname):
    try:
        user=users.models.User.objects.get(email=useremail)
        if user.has_perm('users.'+permissionname):
            content_type = ContentType.objects.get_for_model(users.models.User)
            permission = Permission.objects.get(
            codename=str(permissionname),
            content_type=content_type,
)
            user.user_permissions.remove(permission)
            user=users.models.User.objects.get(email=useremail)
            if not user.has_perm('users.'+permissionname):
                return 'OK'
            else:
                return 'Error'
        return 'OK'
    except:
        return "Error please check permissionname"

    
def VIT_delpermissionall(useremail):
    user=users.models.User.objects.get(email=useremail)
    user.user_permissions.clear()
    user.save()
    return 'OK'

def VIT_addpermissionall(useremail):
    try:
        permissions = [item[0] for item in users.models.User._meta.permissions]
        user=users.models.User.objects.get(email=useremail)
        content_type = ContentType.objects.get_for_model(users.models.User)
        for i in permissions:
            if not user.has_perm('users.'+i):
                permission = Permission.objects.get(
                    codename=str(i),
                    content_type=content_type,
                                                    )
                user.user_permissions.add(permission)
                user=users.models.User.objects.get(email=useremail)
                if user.has_perm('users.'+i):
                    print(i+'----OK')
                else:
                    print(i+'----Error')
        print('success VIT_addpermissionall')
    except:
        return "Error VIT_addpermissionall"

def VIT_L1permission(useremail):
    permissionlist=[
    'projects_projectlist_get',
    'projects_project_get',
    'data_manager_view_get',
    'data_manager_action_get',
    'tasks_taskslist_get',
    'tasks_get'
    ]
    try:
        content_type = ContentType.objects.get_for_model(users.models.User)
        user=users.models.User.objects.get(email=useremail)
        for i in permissionlist:
            if not user.has_perm('users.'+i):
                permission = Permission.objects.get(
                    codename=str(i),
                    content_type=content_type,
                    )
                user.user_permissions.add(permission)
                user=users.models.User.objects.get(email=useremail)
                if user.has_perm('users.'+i):
                    print(i+'----OK')
                else:
                    print(i+'----Error')
        print('success')
    except:
        return "Error"

def VIT_L2permission(useremail):
    permissionlist=[
    'projects_projectlist_get',
    'projects_project_get',
    'data_manager_view_get',
    'data_manager_action_get',
    'tasks_taskslist_get',
    'tasks_get',
    'tasks_annotations_put',
    'tasks_annotations_patch',
    'tasks_annotationlist_post',
    ]
    try:
        content_type = ContentType.objects.get_for_model(users.models.User)
        user=users.models.User.objects.get(email=useremail)
        for i in permissionlist:
            if not user.has_perm('users.'+i):
                permission = Permission.objects.get(
                    codename=str(i),
                    content_type=content_type,
                    )
                user.user_permissions.add(permission)
                user=users.models.User.objects.get(email=useremail)
                if user.has_perm('users.'+i):
                    print(i+'----OK')
                else:
                    print(i+'----Error')
        print('success')
    except:
        return "Error"

def VIT_L3permission(useremail):
    permissionlist=[
    'projects_projectlist_get',
    'projects_project_get',
    'data_manager_view_get',
    'data_manager_action_get',
    'tasks_taskslist_get',
    'tasks_get',
    'tasks_annotations_put',
    'tasks_annotations_patch',
    'tasks_annotationlist_post',
    'tasks_annotations_super',
    ]
    try:
        content_type = ContentType.objects.get_for_model(users.models.User)
        user=users.models.User.objects.get(email=useremail)
        for i in permissionlist:
            if not user.has_perm('users.'+i):
                permission = Permission.objects.get(
                    codename=str(i),
                    content_type=content_type,
                    )
                user.user_permissions.add(permission)
                user=users.models.User.objects.get(email=useremail)
                if user.has_perm('users.'+i):
                    print(i+'----OK')
                else:
                    print(i+'----Error')
        print('success')
    except:
        return "Error"

def VIT_L4permission(useremail):
    try:
        VIT_addpermissionall(useremail)
        return 'success VIT_L4permission'
    except:
        return "Error VIT_L4permission"
    

