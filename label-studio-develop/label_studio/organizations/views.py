"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from organizations.models import Organization
from users.models import User
from django.http import HttpResponse
from organizations.functions import create_organization,destroy_organization,VIT_addusertoorganization,VIT_delusertoorganization,VIT_moveusertoorganization
from users.functions import VIT_L1permission,VIT_L2permission,VIT_L3permission,VIT_L4permission,VIT_delpermissionall


@login_required
def organization_people_list(request):
    return render(request, 'organizations/people_list.html')


@login_required
def simple_view(request):
    return render(request, 'organizations/people_list.html')

@login_required
def orglist_view(request):
        org=Organization.objects.all()
        return render(request, 'organizations/orgpeople.html', {'queryset': org})

@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def userlist_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/userlist.html')
    if request.method == 'POST':
        try:
            orgtitle = request.POST.get('orgtitle')
            org = Organization.objects.get(title=orgtitle)
            queryset = org.users.all()
            return render(request, 'organizations/userlist.html', {'queryset': queryset})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)
        
@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def userinfo_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/userinfo.html')
    if request.method == 'POST':
        try:
            useremail = request.POST.get('useremail')
            user = User.objects.get(email=str(useremail))
            email=user.email
            acorg=user.active_organization
            return render(request, 'organizations/userinfo.html', {'email': email,'acorg': acorg})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)
    
@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def createorg_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/createorg.html')
    if request.method == 'POST':
            title = request.POST.get('title')
            useremail = request.POST.get('useremail')
            user = User.objects.get(email=str(useremail))
            try:
                user.organization
                error_message = "错误！请检查创建者,组织的创建者是唯一的"
                return HttpResponse(error_message)
            except:
                org=create_organization(title,user)
                return render(request, 'organizations/createorg.html', {'org': org})
    error_message = "错误！请检查自己的提交数据"
    return HttpResponse(error_message)
        
@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def delorg_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/delorg.html')
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            org=Organization.objects.get(title=title)
            user=org.created_by
            destroy_organization(org)
            user.organization=None
            return render(request, 'organizations/delorg.html', {'title': title})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)
       
@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def adduser_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/adduser.html')
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            useremail = request.POST.get('useremail')
            user = User.objects.get(email=str(useremail))
            if VIT_addusertoorganization(user,title):
                return render(request, 'organizations/adduser.html', {'item': user})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)

@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def deluser_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/deluser.html')
    if request.method == 'POST':
        try:
            useremail = request.POST.get('useremail')
            user = User.objects.get(email=str(useremail))
            if VIT_delusertoorganization(user):
                return render(request, 'organizations/deluser.html', {'item': user})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)

@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def moveuser_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/moveuser.html')
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            useremail = request.POST.get('useremail')
            user = User.objects.get(email=str(useremail))
            if VIT_moveusertoorganization(user,title):
                return render(request, 'organizations/moveuser.html', {'item': user})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)

@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def userpermissions_view(request):
    if request.method == 'GET':
        return render(request, 'organizations/userpermissions.html')
    if request.method == 'POST':
        try:
            useremail = request.POST.get('useremail')
            user = User.objects.get(email=str(useremail))
            queryset= user.user_permissions.all()
            return render(request, 'organizations/userpermissions.html', {'result': queryset})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)

@permission_required('auth.is_superuser', raise_exception=True)
@login_required
def editpermissions_view(request):
    def process_permission(permission_level, user_email):
        match permission_level:
            case "L1":
                VIT_L1permission(user_email)
            case "L2":
                VIT_L2permission(user_email)
            case "L3":
                VIT_L3permission(user_email)
            case "L4":
                VIT_L4permission(user_email)
            case "del":
                VIT_delpermissionall(user_email)
            case _:
                raise ValueError("Invalid permission level")
    if request.method == 'GET':
        return render(request, 'organizations/editpermissions.html')
    if request.method == 'POST':
        try:
            useremail = request.POST.get('useremail')
            permissionlevel = request.POST.get('type')
            process_permission(permissionlevel,useremail)
            user = User.objects.get(email=str(useremail))
            queryset= user.user_permissions.all()
            return render(request, 'organizations/editpermissions.html', {'result': queryset})
        except:
            error_message = "错误！请检查自己的提交数据"
            return HttpResponse(error_message)