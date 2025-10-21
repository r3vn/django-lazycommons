import json

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

@admin.action(description="Duplicate selected Item(s)")
def duplicate_action(modeladmin, request, queryset):
    """
    Duplicate selected objects admin action.
    """
    for object in queryset:
        object.id = None
        object.save()

def linkify(field_path: str) -> str:
    """
    Converts a foreign key value into clickable links on django admin.
    
    If field_path is 'parent.child', link text will be str(obj.parent.child)
    Link will be the admin url for obj.parent.child.id:change
    """
    def _linkify(obj):
        # Traverse the field path to get the related object
        related_obj = obj
        try:
            for part in field_path.split('.'):
                related_obj = getattr(related_obj, part)
                if related_obj is None:
                    return '-'
        except AttributeError:
            return '-'

        # Build the admin change URL
        app_label = related_obj._meta.app_label
        model_name = related_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[related_obj.pk])

        return format_html('<a href="{}">{}</a>', link_url, related_obj)

    _linkify.short_description = field_path.replace('.', ' -> ')  # Sets column name
    return _linkify

# https://stackoverflow.com/a/72256767
class PrettyJSONEncoder(json.JSONEncoder):
    """
    Pretty encode json fields on django admin.
    """
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)
