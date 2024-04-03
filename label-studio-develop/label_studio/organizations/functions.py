from core.utils.common import temporary_disconnect_all_signals
from django.db import transaction
from organizations.models import Organization, OrganizationMember
from projects.models import Project


def create_organization(title, created_by):
    with transaction.atomic():
        org = Organization.objects.create(title=title, created_by=created_by)
        OrganizationMember.objects.create(user=created_by, organization=org)
        return org


def destroy_organization(org):
    with temporary_disconnect_all_signals():
        Project.objects.filter(organization=org).delete()
        if hasattr(org, 'saml'):
            org.saml.delete()
        org.delete()
        
def VIT_addusertoorganization(user,org_title):
    with transaction.atomic():
        if org_title==user.active_organization:
            return "ok"
        addorg=Organization.objects.get(title=org_title)
        delorg=Organization.objects.get(organization=user.active_organization)
        delorg.remove_user(user)
        addorg.add_user(user)
        user.active_organization = addorg
        user.save(update_fields=['active_organization'])
    return "ok"

def VIT_delusertoorganization(user,org_title):
    with transaction.atomic():
        delorg=Organization.objects.get(title=org_title)
        if delorg.title=="TempOrganization":
            return "ok"
        addorg=Organization.objects.get(title='TempOrganization')
        delorg.remove_user(user)
        addorg.add_user(user)
        user.active_organization = addorg
        user.save(update_fields=['active_organization'])
    return "ok"

        