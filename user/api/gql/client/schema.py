from graphene import Field, ObjectType
from graphene_django import DjangoObjectType

from user.models import User, Admin


class ClientUserType(DjangoObjectType):
    employee = Field("employee.api.gql.client.schema.ClientEmployeeType")
    employer = Field("employer.api.gql.client.schema.ClientEmployerType")
    seller = Field("seller.api.gql.client.schema.ClientSellerType")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "national_id", "mobile", "thumbnail", "birthdate", "sex", "employee",
                  "employer", "seller", "email"]


class ClientPublicUserType(DjangoObjectType):
    """
    for public information of user
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "thumbnail", "sex"]


class ClientAdminType(DjangoObjectType):
    user = Field(ClientPublicUserType)

    class Meta:
        model = Admin
        fields = ["id", "user"]


class Query(ObjectType):
    client_me = Field(ClientUserType)

    def resolve_client_me(root, info, **kwargs):
        return info.context.user
