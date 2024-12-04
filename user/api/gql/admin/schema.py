from graphene import ObjectType, String, Field, Boolean, List
from graphene_django import DjangoObjectType

from user.models import User, Admin
from utils.gql.decorators import super_admin_check_permission
from utils.gql.graphql_pagination import DjangoPaginationConnectionField


class AdminUserType(DjangoObjectType):
    customer = Field("customer.api.gql.client.schema.AdminCustomerType")
    is_admin = Boolean()
    is_employee = Boolean()
    is_employer = Boolean()

    class Meta:
        model = User
        fields = '__all__'
        filter_fields = {
            'id': ['exact', 'in'],
            'first_name': ['exact', 'icontains', 'in'],
            'last_name': ['exact', 'icontains', 'in'],
            'national_id': ['exact', 'icontains', 'in'],
            'mobile': ['exact', 'icontains', 'in'],
            'employee': ['exact', 'isnull'],
            'client': ['exact', 'isnull'],
            'employer': ['exact', 'isnull'],
        }

    def resolve_is_admin(self, info):
        return hasattr(self, 'client')

    def resolve_is_employee(self, info):
        return hasattr(self, 'employee')

    def resolve_is_employer(self, info):
        return hasattr(self, 'employer')


class AdminAdminType(DjangoObjectType):
    user = Field(AdminUserType)

    class Meta:
        model = Admin
        fields = '__all__'
        filter_fields = {
            'id': ['exact', 'in'],
            'group': ['exact', 'in'],
        }


class Query(ObjectType):
    admin_users = DjangoPaginationConnectionField(AdminUserType, search=String(required=False))
    admins = DjangoPaginationConnectionField(AdminAdminType, search=String(required=False))
    admin_me = Field(AdminAdminType)

    @super_admin_check_permission
    def resolve_admin_users(root, info, search=None, **kwargs):
        if search is not None:
            return User.objects.search(query=search)
        return User.objects.all()

    @super_admin_check_permission
    def resolve_admins(root, info, search=None, **kwargs):
        if search:
            return Admin.objects.filter(user__in=User.objects.search(query=search))
        return Admin.objects.all()

    def resolve_admin_me(root, info, **kwargs):
        return Admin.objects.get(user=info.context.user)

