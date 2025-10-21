import uuid
from django.db import models

class UUID4Model(models.Model):
    """
    Abstract Model with UUID4 as primary key. 
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract=True
