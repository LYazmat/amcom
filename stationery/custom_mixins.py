from typing import List, Dict, Type, Any
from django.db.models.query import QuerySet
from rest_framework.serializers import Serializer


class CUDNestedMixin(object):
    '''
    Create-Update[PUT]-Delete Mixin for NestedSerializers
    Keep in mind that partial updates [PATCH] will treats each nested object apart
    When using this mixin, that means it will commit updates and deletes on
    existing objects even when a new object raises an excepetion when creating
    Thus, you may want deny patch / update partial from view

    A empty list [] will remove all items by default
    '''
    @staticmethod
    def cud_nested(
        queryset: QuerySet,
        data: List[Dict],
        serializer: Type[Serializer],
        context: Dict,
        related: Dict[str, Any]
    ):
        '''
        Logic for handling multiple updates, creates and deletes on nested resources
        :param queryset: queryset for objects existing in DB
        :param data: initial data to validate passed from higher level serializer to nested serializer
        :param serializer: nested serializer to use
        :param context: context passed from higher level serializer
        :param related: dict contains related model field and id
        :return N/A
        '''
        updated_ids = list()
        for_create = list()
        for item in data:
            item.update(related)
            item_id = item.get("id")
            if item_id:
                instance = queryset.get(id=item_id)
                update_serializer = serializer(
                    instance=instance, data=item, context=context
                )
                update_serializer.is_valid(raise_exception=True)
                update_serializer.save()
                updated_ids.append(instance.id)
            else:
                for_create.append(item)

        delete_queryset = queryset.exclude(id__in=updated_ids)
        delete_queryset.delete()

        create_serializer = serializer(
            data=for_create, many=True, context=context)
        create_serializer.is_valid(raise_exception=True)
        create_serializer.save()
