"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging

from core.feature_flags import flag_set
from core.middleware import enforce_csrf_checks
from core.utils.common import load_func
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, reverse
from django.utils.http import is_safe_url
from organizations.forms import OrganizationSignupForm
from organizations.models import Organization
from rest_framework.authtoken.models import Token
from users import forms
from users.functions import login, proceed_registration,VIT_base_proceed_registration

logger = logging.getLogger()


@login_required
def logout(request):
    auth.logout(request)
    if settings.HOSTNAME:
        redirect_url = settings.HOSTNAME
        if not redirect_url.endswith('/'):
            redirect_url += '/'
        return redirect(redirect_url)
    return redirect('/')

#VIT
@enforce_csrf_checks
def user_signup(request):
    """Sign up page"""
    user = request.user
    next_page = request.GET.get('next')
    token = request.GET.get('token')

    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')

    user_form = forms.UserSignupForm()
    organization_form = OrganizationSignupForm()

    if user.is_authenticated:
        return redirect(next_page)

    # make a new user
    if request.method == 'POST':
        organization = Organization.objects.first()
        if settings.DISABLE_SIGNUP_WITHOUT_LINK is True:
            if not (token and organization and token == organization.token):
                raise PermissionDenied()
        else:
            if token and organization and token != organization.token:
                raise PermissionDenied()

        user_form = forms.UserSignupForm(request.POST)
        organization_form = OrganizationSignupForm(request.POST)

        if user_form.is_valid():
            redirect_response = VIT_base_proceed_registration(request, user_form, organization_form, next_page)
            if redirect_response:
                return redirect_response

    if flag_set('fflag_feat_front_lsdv_e_297_increase_oss_to_enterprise_adoption_short'):
        return render(
            request,
            'users/new-ui/user_signup.html',
            {
                'user_form': user_form,
                'organization_form': organization_form,
                'next': next_page,
                'token': token,
            },
        )

    return render(
        request,
        'users/user_signup.html',
        {
            'user_form': user_form,
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )



@enforce_csrf_checks
def user_login(request):
    """Login page"""
    user = request.user
    next_page = request.GET.get('next')

    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')

    login_form = load_func(settings.USER_LOGIN_FORM)
    form = login_form()

    if user.is_authenticated:
        return redirect(next_page)

    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if form.cleaned_data['persist_session'] is not True:
                # Set the session to expire when the browser is closed
                request.session['keep_me_logged_in'] = False
                request.session.set_expiry(0)

            # user is organization member
            org_pk = Organization.find_by_user(user).pk
            user.active_organization_id = org_pk
            user.save(update_fields=['active_organization'])
            return redirect(next_page)

    if flag_set('fflag_feat_front_lsdv_e_297_increase_oss_to_enterprise_adoption_short'):
        return render(request, 'users/new-ui/user_login.html', {'form': form, 'next': next_page})

    return render(request, 'users/user_login.html', {'form': form, 'next': next_page})


@login_required
def user_account(request):
    user = request.user

    if user.active_organization is None and 'organization_pk' not in request.session:
        return redirect(reverse('main'))

    form = forms.UserProfileForm(instance=user)
    token = Token.objects.get(user=user)

    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('user-account'))

    return render(
        request,
        'users/user_account.html',
        {'settings': settings, 'user': user, 'user_profile_form': form, 'token': token},
    )
    
@enforce_csrf_checks
def VIT_super_user_signup(request):

    user = request.user
    next_page = request.GET.get('next')
    token = request.GET.get('token')

    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')

#当用户首次访问包含表单的页面时，我们需要创建一个空的表单对象，
#以便将其传递给模板并在页面上呈现出来，让用户填写信息。
    user_form = forms.VIT_super_UserSignupForm()
    organization_form = OrganizationSignupForm()

    if user.is_authenticated:
        return redirect(next_page)

    # make a new user
    if request.method == 'POST':
        organization = Organization.objects.first()
        if settings.DISABLE_SIGNUP_WITHOUT_LINK is True:
            if not (token and organization and token == organization.token):
                raise PermissionDenied()
        else:
            if token and organization and token != organization.token:
                raise PermissionDenied()
                
#当用户提交表单后，我们需要使用用户提交的数据（通常在 request.POST 中）
#来填充表单对象，并进行验证。
        user_form = forms.VIT_super_UserSignupForm(request.POST)
        organization_form = OrganizationSignupForm(request.POST)

        if user_form.is_valid():
            #proceed_registration注册用户的函数
            redirect_response = VIT_super_proceed_registration(request, user_form, organization_form, next_page)
            if redirect_response:
                return redirect_response

    return render(
        request,
        'users/super_user_signup.html',
        {
            'user_form': user_form,
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_adduser(request):

    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
#当用户首次访问包含表单的页面时，我们需要创建一个空的表单对象，
#以便将其传递给模板并在页面上呈现出来，让用户填写信息。
    user_form = forms.UserSignupForm()
    organization_form = OrganizationSignupForm()
    # make a new user
    if request.method == 'POST':
#当用户提交表单后，我们需要使用用户提交的数据（通常在 request.POST 中）
#来填充表单对象，并进行验证。
        user_form = forms.UserSignupForm(request.POST)
        organization_form = OrganizationSignupForm(request.POST)
        if user_form.is_valid():
            #proceed_registration注册用户的函数
            redirect_response = VIT_base_proceed_registration(request, user_form, organization_form, next_page)
            if redirect_response:
                return JsonResponse({'message': '用户添加成功'})

    if flag_set('fflag_feat_front_lsdv_e_297_increase_oss_to_enterprise_adoption_short'):
        return render(
            request,
            'users/new-ui/user_signup.html',
            {
                'user_form': user_form,
                'organization_form': organization_form,
                'next': next_page,
                'token': token,
            },
        )

    return render(
        request,
        'users/super_user_adduser.html',
        {
            'user_form': user_form,
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_deluser(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    # make a new user
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        deluser  = User.objects.filter(email=str(user_email))
        if deluser:
            deluser.delete()
            return HttpResponse("<p>用户删除成功</p>")
        else:
            return JsonResponse({'message': '用户不存在，删除失败'}, status=400)

    return render(
        request,
        'users/super_user_deluser.html',
        {
            'next': next_page,
            'token': token,
        },
    )

    
@login_required
def VIT_super_user_findalluser(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    # make a new user
    listuser = None
    if request.method == 'POST':
        listuser = User.objects.all()
        context = {'listuser': list(listuser)} 
    return render(
        request,
        'users/super_user_findalluser.html',
        {
            'listuser': context,  # 将用户列表传递到模板中
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_finduser(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    # make a new user
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        finduser  = User.objects.filter(email=str(user_email)).first()
        if finduser is None:
            return JsonResponse({'message': '用户不存在'}, status=400)

    return render(
        request,
        'users/super_user_finduser.html',
        {
            'user': finduser,  # 将用户列表传递到模板中
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_creorg(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
#当用户首次访问包含表单的页面时，我们需要创建一个空的表单对象，
#以便将其传递给模板并在页面上呈现出来，让用户填写信息。
    organization_form = VIT_OrganizationForm()
    # make a new user
    if request.method == 'POST':
#当用户提交表单后，我们需要使用用户提交的数据（通常在 request.POST 中）
#来填充表单对象，并进行验证。
        organization_form = VIT_OrganizationForm(request.POST)
        if organization_form.is_valid():  # 验证表单数据的有效性
            create_organization(organization_form.title, created_by=user)
            return JsonResponse({'message': '创建成功'})

    return render(
        request,
        'users/super_user_creorg.html',
        {
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_delorg(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    organization_form = VIT_OrganizationForm()
    if request.method == 'POST':
        organization_form = VIT_OrganizationForm(request.POST)
        if organization_form.is_valid():  # 验证表单数据的有效性
            org=Organization.objects.get(title=str(organization_form.title))
            destroy_organization(org)
            return JsonResponse({'message': '删除成功'})

    return render(
        request,
        'users/super_user_creorg.html',
        {
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_addtoorg(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    user_form = forms.VIT_super_UserForm()
    organization_form = VIT_OrganizationForm()
    # make a new user
    if request.method == 'POST':
        user_form = forms.VIT_super_UserForm(request.post)
        organization_form = VIT_OrganizationForm(request.post)
        if user_form.is_valid() and organization_form.is_valid():
            redirect_response = VIT_super_proceed_useraddorg(request, user_form, organization_form, next_page)
            if  redirect_response:
                return redirect_response

    return render(
        request,
        'users/super_user_adduser.html',
        {
            'user_form': user_form,
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_deltoorg(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    user_form = forms.VIT_super_UseraddForm()
    organization_form = VIT_OrganizationForm()
    # make a new user
    if request.method == 'POST':
        user_form = forms.VIT_super_UserSignupForm(request.post)
        organization_form = VIT_OrganizationForm(request.post)
        if user_form.is_valid() and organization_form.is_valid():
            redirect_response = VIT_super_proceed_userdelorg(request, user_form, organization_form, next_page)
            if  redirect_response:
                return redirect_response

    return render(
        request,
        'users/super_user_adduser.html',
        {
            'user_form': user_form,
            'organization_form': organization_form,
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_findorg(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    # make a new user
    if request.method == 'POST':
        orgtitle = request.POST.get('organization_title')
        findorg  = Organization.objects.filter(title=str(orgtitle)).first()
        if findorg is None:
            return JsonResponse({'message': '用户不存在'}, status=400)
    return render(
        request,
        'users/super_user_findorg.html',
        {
            'org': findorg,  # 将用户列表传递到模板中
            'next': next_page,
            'token': token,
        },
    )

@login_required
def VIT_super_user_finalldorg(request):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied()
    next_page = request.GET.get('next')
    token = request.GET.get('token')
    # checks if the URL is a safe redirection.
    if not next_page or not is_safe_url(url=next_page, allowed_hosts=request.get_host()):
        next_page = reverse('projects:project-index')
    # make a new user
    orglist=None
    if request.method == 'POST':
        orglist  = Organization.objects.all()
        context = {'listorg': list(orglist)} 
        if orglist is None:
            return JsonResponse({'message': '没有组织'}, status=400)
    return render(
        request,
        'users/super_user_findorg.html',
        {
            'org': context,  # 将用户列表传递到模板中
            'next': next_page,
            'token': token,
        },
    )