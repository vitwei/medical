"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from django.urls import include, path
from organizations import api, views

app_name = 'organizations'

# TODO: there should be only one patterns list based on API (with api/ prefix removed)
# Page URLs
_urlpatterns = [
    # get organization page
    path('', views.organization_people_list, name='organization-index'),
]

# API URLs
_api_urlpattens = [
    # organization list viewset
    path('', api.OrganizationListAPI.as_view(), name='organization-list'),
    # organization detail viewset
    path('<int:pk>', api.OrganizationAPI.as_view(), name='organization-detail'),
    # organization memberships list viewset
    path('<int:pk>/memberships', api.OrganizationMemberListAPI.as_view(), name='organization-memberships-list'),
    path(
        '<int:pk>/memberships/<int:user_pk>/',
        api.OrganizationMemberDetailAPI.as_view(),
        name='organization-membership-detail',
    ),
]
# TODO: these urlpatterns should be moved in core/urls with include('organizations.urls')
urlpatterns = [
    path('organization/', views.simple_view, name='organization-simple'),
    path('orglist/', views.orglist_view, name='organization-list'),
    path('orglist/userlist', views.userlist_view, name='organization-people'),
    path('orglist/userinfo', views.userinfo_view, name='organization-peopleinfo'),
    path('orglist/createorg', views.createorg_view, name='organization-create'),
    path('orglist/delorg', views.delorg_view, name='organization-del'),
    path('orglist/adduser', views.adduser_view, name='user-add'),
    path('orglist/deluser', views.deluser_view, name='user-del'),
    path('orglist/moveuser', views.moveuser_view, name='user-move'),    
    path('orglist/userpermission', views.userpermissions_view, name='user-move'),
    path('organization/webhooks', views.simple_view, name='organization-simple-webhooks'),
    path('people/', include(_urlpatterns)),
    # TODO: temporary route, remove as needed
    path('models/', views.simple_view, name='models'),
    path('api/organizations/', include((_api_urlpattens, app_name), namespace='api')),
    # invite
    path('api/invite', api.OrganizationInviteAPI.as_view(), name='organization-invite'),
    path('api/invite/reset-token', api.OrganizationResetTokenAPI.as_view(), name='organization-reset-token'),
]
