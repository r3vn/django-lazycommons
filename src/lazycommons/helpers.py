from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

def get_sentinel_user() -> User:
    """
    Prevent model instance removal when deleting an user
    """
    return get_user_model().objects.get_or_create(username="deleted")[0]

def queryset_to_dicts(queryset, include_m2m=False):
    """
    Serialize a generic queryset into a list of dictionaries
    """
    model = queryset.model
    meta = model._meta

    fields = [field for field in meta.fields]

    data = []

    for obj in queryset:
        row = {}

        for field in fields:
            # Choices: use get_FOO_display()
            if field.choices:
                display_method = "get_%s_display" % field.name
                if hasattr(obj, display_method):
                    value = getattr(obj, display_method)()
                else:
                    value = getattr(obj, field.name)

            # ForeignKey: string representation
            elif isinstance(field, models.ForeignKey):
                fk_obj = getattr(obj, field.name)
                value = str(fk_obj) if fk_obj else None

            # Default field
            else:
                value = getattr(obj, field.name)

            row[field.name] = value

        if include_m2m:
            for field in meta.many_to_many:
                row[field.name] = [
                    str(x) for x in getattr(obj, field.name).all()
                ]

        data.append(row)

    return data, [f.name for f in fields]
