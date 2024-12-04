import math

from graphene import ObjectType, Boolean
from graphene import Int, String
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.utils import maybe_queryset
from django.core.paginator import Paginator
import re

from collections import OrderedDict
from graphene import Connection, List, NonNull, Field
from graphene.relay.connection import ConnectionOptions


class PageInfoExtra(ObjectType):
    has_next_page = Boolean(
        required=True,
        name="hasNextPage",
        description="When paginating forwards, are there more items?",
    )

    has_previous_page = Boolean(
        required=True,
        name="hasPreviousPage",
        description="When paginating backwards, are there more items?",
    )


class PaginationConnection(Connection):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, node=None, name=None, **options):
        _meta = ConnectionOptions(cls)
        base_name = re.sub("Connection$", "", name or cls.__name__) or node._meta.name  # noqa

        if not name:
            name = "{}Connection".format(base_name)

        options["name"] = name
        _meta.node = node
        _meta.fields = OrderedDict(
            [
                (
                    "page_info",
                    Field(
                        PageInfoExtra,
                        name="pageInfo",
                        required=True,
                        description="Pagination data for this connection.",
                    ),
                ),
                (
                    "results",
                    Field(
                        NonNull(List(node)),
                        description="Contains the nodes in this connection.",
                    ),
                ),
            ]
        )

        return super(Connection, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )


class DjangoPaginationConnectionField(DjangoFilterConnectionField):
    def __init__(
            self,
            type,
            fields=None,
            order_by=None,
            extra_filter_meta=None,
            filterset_class=None,
            *args,
            **kwargs
    ):
        self._type = type
        self._fields = fields
        self._provided_filterset_class = filterset_class
        self._filterset_class = None
        self._extra_filter_meta = extra_filter_meta
        self._base_args = None

        kwargs.setdefault("limit", Int(description="Query limit"))
        kwargs.setdefault("offset", Int(description="Query offset"))
        kwargs.setdefault("ordering", String(description="Query order"))

        super(DjangoPaginationConnectionField, self).__init__(
            type,
            *args,
            **kwargs
        )

    @property
    def type(self):
        class NodeConnection(PaginationConnection):
            total_count = Int()

            class Meta:
                node = self._type
                name = '{}NodeConnection'.format(self._type._meta.name)

            def resolve_total_count(self, info, **kwargs):
                return self.iterable.count()

        return NodeConnection

    @classmethod
    def resolve_connection(cls, connection, *args, **kwargs):
        arguments = args[0]
        iterable = args[1]

        iterable = maybe_queryset(iterable)

        _len = len(iterable)

        ordering = arguments.get("ordering")

        if ordering:
            iterable = connection_from_list_ordering(iterable, ordering)

        connection = connection_from_list_slice(
            iterable,
            arguments,
            connection_type=connection,
            pageinfo_type=PageInfoExtra,
        )
        connection.iterable = iterable
        connection.length = _len

        return connection


def connection_from_list_slice(
        list_slice, args=None, connection_type=None, pageinfo_type=None
):
    args = args or {}
    limit = args.get("limit", 100)
    offset = args.get("offset", 0)

    assert isinstance(limit, int), "Limit must be of type int"
    assert limit > 0, "Limit must be positive integer greater than 0"

    paginator = Paginator(list_slice, limit)
    _slice = list_slice[offset:(offset + limit)]

    page_num = math.ceil(offset / limit) + 1
    page_num = (
        paginator.num_pages
        if page_num > paginator.num_pages
        else page_num
    )
    page = paginator.page(page_num)

    return connection_type(
        results=_slice,
        page_info=pageinfo_type(
            has_previous_page=page.has_previous(),
            has_next_page=page.has_next()
        )
    )


def connection_from_list_ordering(items_list, ordering):
    field, order = ordering.split(',')

    order = '-' if order == 'desc' else ''
    field = re.sub(r'(?<!^)(?=[A-Z])', '_', field).lower()

    return items_list.order_by(f'{order}{field}')
