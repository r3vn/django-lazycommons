from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def get_sentinel_user() -> User:
    """
    Prevent model instance removal when deleting an user
    """
    return get_user_model().objects.get_or_create(username="deleted")[0]
